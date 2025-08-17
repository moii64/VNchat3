from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from app.core.config import settings
from app.api.routes import chat, documents, conversations, health
from app.core.database import engine
from app.models import base

# Create database tables
base.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Intelligent Chatbot API",
    description="AI-powered chatbot with RAG capabilities",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(documents.router, prefix="/api", tags=["documents"])
app.include_router(conversations.router, prefix="/api", tags=["conversations"])

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
