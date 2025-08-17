from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.chat_service import ChatService
from app.services.vector_service import VectorService

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: int
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    answer: str
    conversation_id: int
    message_id: int
    sources: List[str] = []
    tokens_used: Optional[int] = None

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """Chat endpoint with RAG capabilities"""
    try:
        chat_service = ChatService(db)
        vector_service = VectorService()
        
        # Get relevant documents using RAG
        relevant_docs = await vector_service.search_documents(request.message, top_k=3)
        
        # Generate response using LLM
        response = await chat_service.generate_response(
            user_id=request.user_id,
            message=request.message,
            conversation_id=request.conversation_id,
            context_docs=relevant_docs
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@router.get("/chat/history/{user_id}")
async def get_chat_history(
    user_id: int,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get chat history for a user"""
    try:
        chat_service = ChatService(db)
        history = await chat_service.get_user_history(user_id, limit)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")
