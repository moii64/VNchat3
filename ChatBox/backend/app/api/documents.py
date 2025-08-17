from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.document_service import DocumentService

router = APIRouter()

class DocumentResponse(BaseModel):
    id: int
    title: str
    source: str
    document_type: str
    created_at: str

@router.post("/documents/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Ingest a new document into the system"""
    try:
        document_service = DocumentService(db)
        
        # Validate file type
        if not file.filename.endswith(('.txt', '.md', '.pdf')):
            raise HTTPException(
                status_code=400, 
                detail="Only .txt, .md, and .pdf files are supported"
            )
        
        # Process and store document
        result = await document_service.ingest_document(file)
        
        return {
            "message": "Document ingested successfully",
            "document_id": result["document_id"],
            "chunks_created": result["chunks_created"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion error: {str(e)}")

@router.get("/documents", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all documents in the system"""
    try:
        document_service = DocumentService(db)
        documents = await document_service.list_documents(skip, limit)
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")

@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """Delete a document from the system"""
    try:
        document_service = DocumentService(db)
        await document_service.delete_document(document_id)
        return {"message": "Document deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")
