from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.conversation import Conversation
from app.models.message import Message

class ConversationService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_user_conversations(
        self, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get conversations for a user with message count"""
        conversations = self.db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).offset(skip).limit(limit).all()
        
        result = []
        for conv in conversations:
            # Get message count
            message_count = self.db.query(Message).filter(
                Message.conversation_id == conv.id
            ).count()
            
            result.append({
                "id": conv.id,
                "title": conv.title,
                "summary": conv.summary,
                "created_at": conv.created_at.isoformat(),
                "message_count": message_count
            })
        
        return result
    
    async def get_conversation_messages(self, conversation_id: int) -> List[Dict[str, Any]]:
        """Get all messages in a conversation"""
        messages = self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc()).all()
        
        return [
            {
                "id": msg.id,
                "role": msg.role.value,
                "content": msg.content,
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]
    
    async def delete_conversation(self, conversation_id: int) -> bool:
        """Delete a conversation and all its messages"""
        try:
            conversation = self.db.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()
            
            if not conversation:
                return False
            
            # Messages will be deleted automatically due to cascade
            self.db.delete(conversation)
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Conversation deletion failed: {str(e)}")
    
    async def update_title(self, conversation_id: int, title: str) -> bool:
        """Update conversation title"""
        try:
            conversation = self.db.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()
            
            if not conversation:
                return False
            
            conversation.title = title
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Title update failed: {str(e)}")
    
    async def get_conversation_summary(self, conversation_id: int) -> str:
        """Generate a summary of the conversation"""
        try:
            messages = self.db.query(Message).filter(
                Message.conversation_id == conversation_id
            ).order_by(Message.created_at.asc()).all()
            
            if not messages:
                return "Không có tin nhắn nào trong cuộc hội thoại này."
            
            # Simple summary based on first and last messages
            first_msg = messages[0].content[:100] + "..." if len(messages[0].content) > 100 else messages[0].content
            last_msg = messages[-1].content[:100] + "..." if len(messages[-1].content) > 100 else messages[-1].content
            
            return f"Cuộc hội thoại bắt đầu với: '{first_msg}' và kết thúc với: '{last_msg}'"
            
        except Exception as e:
            return f"Không thể tạo tóm tắt: {str(e)}"
    
    async def search_conversations(
        self, 
        user_id: int, 
        query: str, 
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search conversations by content"""
        try:
            # Search in message content
            messages = self.db.query(Message).join(Conversation).filter(
                Conversation.user_id == user_id,
                Message.content.ilike(f"%{query}%")
            ).limit(limit).all()
            
            # Group by conversation
            conversation_ids = set()
            for msg in messages:
                conversation_ids.add(msg.conversation_id)
            
            # Get conversation details
            conversations = []
            for conv_id in conversation_ids:
                conv = self.db.query(Conversation).filter(Conversation.id == conv_id).first()
                if conv:
                    conversations.append({
                        "id": conv.id,
                        "title": conv.title,
                        "created_at": conv.created_at.isoformat()
                    })
            
            return conversations
            
        except Exception as e:
            return []
