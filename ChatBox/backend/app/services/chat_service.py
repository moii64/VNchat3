import openai
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.conversation import Conversation
from app.models.message import Message, MessageRole
from app.models.user import User
from datetime import datetime

class ChatService:
    def __init__(self, db: Session):
        self.db = db
        openai.api_key = settings.OPENAI_API_KEY
        
    async def generate_response(
        self,
        user_id: int,
        message: str,
        conversation_id: int = None,
        context_docs: List[str] = []
    ) -> Dict[str, Any]:
        """Generate AI response using LLM with RAG context"""
        
        # Get or create conversation
        if not conversation_id:
            conversation = self._create_conversation(user_id, message)
            conversation_id = conversation.id
        else:
            conversation = self.db.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()
            
        # Save user message
        user_message = Message(
            conversation_id=conversation_id,
            role=MessageRole.USER,
            content=message
        )
        self.db.add(user_message)
        self.db.commit()
        
        # Build prompt with context
        prompt = self._build_prompt(message, context_docs)
        
        try:
            # Generate response using OpenAI
            response = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=500,
                temperature=0.2
            )
            
            answer = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            # Save AI response
            ai_message = Message(
                conversation_id=conversation_id,
                role=MessageRole.ASSISTANT,
                content=answer,
                tokens_used=tokens_used
            )
            self.db.add(ai_message)
            self.db.commit()
            
            return {
                "answer": answer,
                "conversation_id": conversation_id,
                "message_id": ai_message.id,
                "sources": context_docs,
                "tokens_used": tokens_used
            }
            
        except Exception as e:
            # Fallback response
            fallback_answer = "Xin lỗi, tôi đang gặp sự cố. Vui lòng thử lại sau."
            
            ai_message = Message(
                conversation_id=conversation_id,
                role=MessageRole.ASSISTANT,
                content=fallback_answer
            )
            self.db.add(ai_message)
            self.db.commit()
            
            return {
                "answer": fallback_answer,
                "conversation_id": conversation_id,
                "message_id": ai_message.id,
                "sources": [],
                "tokens_used": 0
            }
    
    def _create_conversation(self, user_id: int, first_message: str) -> Conversation:
        """Create a new conversation"""
        # Generate title from first message
        title = first_message[:50] + "..." if len(first_message) > 50 else first_message
        
        conversation = Conversation(
            user_id=user_id,
            title=title
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation
    
    def _build_prompt(self, message: str, context_docs: List[str]) -> str:
        """Build system prompt with RAG context"""
        system_prompt = """Bạn là một trợ lý AI thông minh chuyên về hỗ trợ khách hàng và trả lời câu hỏi.

HƯỚNG DẪN:
1. Sử dụng thông tin từ CONTEXT để trả lời chính xác
2. Nếu không có thông tin phù hợp trong context, hãy nói rõ "Tôi không tìm thấy thông tin phù hợp"
3. Trả lời ngắn gọn, rõ ràng và hữu ích
4. Luôn lịch sự và chuyên nghiệp

CONTEXT:
{context}

Hãy trả lời câu hỏi của người dùng dựa trên thông tin trên."""
        
        context_text = "\n\n".join(context_docs) if context_docs else "Không có tài liệu tham khảo."
        return system_prompt.format(context=context_text)
    
    async def get_user_history(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get chat history for a user"""
        conversations = self.db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(Conversation.created_at.desc()).limit(limit).all()
        
        history = []
        for conv in conversations:
            messages = self.db.query(Message).filter(
                Message.conversation_id == conv.id
            ).order_by(Message.created_at.asc()).all()
            
            history.append({
                "conversation_id": conv.id,
                "title": conv.title,
                "messages": [
                    {
                        "role": msg.role.value,
                        "content": msg.content,
                        "timestamp": msg.created_at.isoformat()
                    }
                    for msg in messages
                ]
            })
        
        return history
