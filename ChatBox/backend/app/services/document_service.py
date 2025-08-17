import os
import PyPDF2
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.models.document import Document
from app.services.vector_service import VectorService
import re

class DocumentService:
    def __init__(self, db: Session):
        self.db = db
        self.vector_service = VectorService()
        
    async def ingest_document(self, file: UploadFile) -> Dict[str, Any]:
        """Ingest a document file into the system"""
        try:
            # Read file content
            content = await self._read_file_content(file)
            
            # Split into chunks
            chunks = self._split_into_chunks(content, chunk_size=1000)
            
            # Store in database and vector store
            document_ids = []
            for i, chunk in enumerate(chunks):
                # Save to database
                doc = Document(
                    title=f"{file.filename} - Chunk {i+1}",
                    content=chunk,
                    source=file.filename,
                    file_path=file.filename,
                    document_type=file.filename.split('.')[-1],
                    chunk_index=i
                )
                self.db.add(doc)
                self.db.commit()
                self.db.refresh(doc)
                
                # Add to vector store
                metadata = {
                    "document_id": doc.id,
                    "title": doc.title,
                    "source": doc.source,
                    "chunk_index": i
                }
                
                vector_id = await self.vector_service.add_document(chunk, metadata)
                
                # Update document with vector store reference
                doc.embedding_id = vector_id
                self.db.commit()
                
                document_ids.append(doc.id)
            
            return {
                "document_id": document_ids[0],  # Return first chunk ID
                "chunks_created": len(chunks),
                "total_chunks": len(chunks)
            }
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Document ingestion failed: {str(e)}")
    
    async def _read_file_content(self, file: UploadFile) -> str:
        """Read content from uploaded file"""
        if file.filename.endswith('.txt') or file.filename.endswith('.md'):
            content = await file.read()
            return content.decode('utf-8')
            
        elif file.filename.endswith('.pdf'):
            content = await file.read()
            pdf_reader = PyPDF2.PdfReader(content)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
            
        else:
            raise ValueError(f"Unsupported file type: {file.filename}")
    
    def _split_into_chunks(self, text: str, chunk_size: int = 1000) -> List[str]:
        """Split text into chunks of specified size"""
        # Simple splitting by sentences
        sentences = re.split(r'[.!?]+', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            if len(current_chunk) + len(sentence) < chunk_size:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        # Add remaining chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    async def list_documents(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """List documents with pagination"""
        documents = self.db.query(Document).offset(skip).limit(limit).all()
        
        return [
            {
                "id": doc.id,
                "title": doc.title,
                "source": doc.source,
                "document_type": doc.document_type,
                "created_at": doc.created_at.isoformat()
            }
            for doc in documents
        ]
    
    async def delete_document(self, document_id: int) -> bool:
        """Delete a document and its chunks"""
        try:
            # Find all chunks of this document
            chunks = self.db.query(Document).filter(
                Document.source == self.db.query(Document.source).filter(
                    Document.id == document_id
                ).first().source
            ).all()
            
            # Delete from vector store
            for chunk in chunks:
                if chunk.embedding_id:
                    self.vector_service.delete_document(chunk.embedding_id)
            
            # Delete from database
            for chunk in chunks:
                self.db.delete(chunk)
            
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Document deletion failed: {str(e)}")
    
    def get_document_stats(self) -> Dict[str, Any]:
        """Get statistics about documents"""
        try:
            total_docs = self.db.query(Document).count()
            doc_types = self.db.query(Document.document_type).distinct().all()
            
            return {
                "total_documents": total_docs,
                "document_types": [dt[0] for dt in doc_types if dt[0]],
                "vector_store_stats": self.vector_service.get_collection_stats()
            }
        except Exception as e:
            return {"error": str(e)}
