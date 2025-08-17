import chromadb
from typing import List, Dict, Any
from app.core.config import settings
import openai
import hashlib

class VectorService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIRECTORY)
        self.collection = self._get_or_create_collection()
        openai.api_key = settings.OPENAI_API_KEY
        
    def _get_or_create_collection(self):
        """Get existing collection or create new one"""
        try:
            collection = self.client.get_collection("documents")
        except:
            collection = self.client.create_collection(
                name="documents",
                metadata={"hnsw:space": "cosine"}
            )
        return collection
    
    async def search_documents(self, query: str, top_k: int = 3) -> List[str]:
        """Search for relevant documents using vector similarity"""
        try:
            # Generate query embedding
            query_embedding = await self._get_embedding(query)
            
            # Search in vector store
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=["documents", "metadatas"]
            )
            
            # Extract document content
            documents = results.get("documents", [[]])
            if documents and documents[0]:
                return documents[0]
            return []
            
        except Exception as e:
            print(f"Vector search error: {e}")
            return []
    
    async def add_document(self, content: str, metadata: Dict[str, Any]) -> str:
        """Add a document to the vector store"""
        try:
            # Generate document embedding
            embedding = await self._get_embedding(content)
            
            # Generate unique ID
            doc_id = hashlib.md5(content.encode()).hexdigest()
            
            # Add to collection
            self.collection.add(
                embeddings=[embedding],
                documents=[content],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            return doc_id
            
        except Exception as e:
            print(f"Error adding document: {e}")
            raise
    
    async def _get_embedding(self, text: str) -> List[float]:
        """Get OpenAI embedding for text"""
        try:
            response = openai.Embedding.create(
                model=settings.OPENAI_EMBEDDING_MODEL,
                input=text
            )
            return response['data'][0]['embedding']
        except Exception as e:
            print(f"Embedding error: {e}")
            # Return zero vector as fallback
            return [0.0] * 1536  # OpenAI ada-002 dimension
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document from vector store"""
        try:
            self.collection.delete(ids=[doc_id])
            return True
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector collection"""
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "collection_name": "documents"
            }
        except Exception as e:
            return {"error": str(e)}
