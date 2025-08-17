from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.conversation_service import ConversationService

router = APIRouter()

class ConversationResponse(BaseModel):
    id: int
    title: str
    summary: Optional[str]
    created_at: str
    message_count: int

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: str

@router.get("/conversations/{user_id}", response_model=List[ConversationResponse])
async def get_user_conversations(
    user_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get all conversations for a user"""
    try:
        conversation_service = ConversationService(db)
        conversations = await conversation_service.get_user_conversations(user_id, skip, limit)
        return conversations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching conversations: {str(e)}")

@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """Get all messages in a conversation"""
    try:
        conversation_service = ConversationService(db)
        messages = await conversation_service.get_conversation_messages(conversation_id)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching messages: {str(e)}")

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """Delete a conversation"""
    try:
        conversation_service = ConversationService(db)
        await conversation_service.delete_conversation(conversation_id)
        return {"message": "Conversation deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting conversation: {str(e)}")

@router.put("/conversations/{conversation_id}/title")
async def update_conversation_title(
    conversation_id: int,
    title: str,
    db: Session = Depends(get_db)
):
    """Update conversation title"""
    try:
        conversation_service = ConversationService(db)
        await conversation_service.update_title(conversation_id, title)
        return {"message": "Title updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating title: {str(e)}")
