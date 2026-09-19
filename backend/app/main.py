from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.database import engine, Base
from backend.app.rag.ingest import ingest_fitness_knowledge
from backend.app.api.routers import (
    auth_router,
    profile_router,
    sessions_router,
    chat_router,
    products_router
)

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fitness AI Chatbot - Intelligent Health & Recommendation System",
    description="AI-powered fitness chatbot delivering personalized workout and nutrition guidance with RAG and dynamic product recommendations.",
    version="1.0.0"
)

# Enable CORS for frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_router, prefix="/api")
app.include_router(profile_router, prefix="/api")
app.include_router(sessions_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(products_router, prefix="/api")

@app.on_event("startup")
def on_startup():
    print("[FastAPI] Starting Fitness AI Chatbot API...")
    try:
        # Ingest RAG knowledge if needed
        ingest_fitness_knowledge()
    except Exception as e:
        print(f"[FastAPI] Warning during knowledge ingestion: {e}")

@app.get("/")
def root():
    return {
        "status": "online",
        "app": "Fitness AI Chatbot - Intelligent Health & Recommendation System",
        "docs": "/docs",
        "model": settings.LLM_MODEL
    }
