from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Document(Base, TimestampMixin):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    source = Column(String(255), nullable=True)
    file_path = Column(String(500), nullable=True)
    chunk_id = Column(String(100), nullable=True)  # For vector store reference
    embedding_id = Column(String(100), nullable=True)  # Vector store ID
    
    # Metadata
    document_type = Column(String(50), nullable=True)
    page_number = Column(Integer, nullable=True)
    chunk_index = Column(Integer, nullable=True)
