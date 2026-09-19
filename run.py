import sys
import os
import time
import argparse
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from backend.app.config import settings
from backend.app.rag.ingest import ingest_fitness_knowledge

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def banner():
    print("""
========================================================================
   [Fitness AI-Chatbot] - Intelligent Health & Recommendation System
   Backend:  FastAPI (JWT Auth, SQLite Memory, ChromaDB RAG)
   Model:    NVIDIA Nemotron 3 Ultra 550B (NIM)
   Frontend: Streamlit Modern Athletic UI
========================================================================
    """)



def run_backend():
    """Run FastAPI uvicorn server"""
    print(f"[Launcher] Starting FastAPI backend on {settings.BACKEND_HOST}:{settings.BACKEND_PORT}...")
    import uvicorn
    uvicorn.run(
        "backend.app.main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=False
    )

def run_frontend():
    """Run Streamlit frontend app"""
    print(f"[Launcher] Starting Streamlit frontend on port {settings.FRONTEND_PORT}...")
    frontend_script = str(BASE_DIR / "frontend" / "app.py")
    subprocess.run([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        frontend_script,
        "--server.port",
        str(settings.FRONTEND_PORT),
        "--server.headless",
        "true"
    ])

def run_both():
    """Run both backend and frontend concurrently"""
    banner()
    print("[Launcher] Pre-populating ChromaDB vector database if needed...")
    ingest_fitness_knowledge()

    print("\n[Launcher] Launching FastAPI backend...")
    backend_proc = subprocess.Popen([
        sys.executable,
        "-m",
        "uvicorn",
        "backend.app.main:app",
        "--host",
        settings.BACKEND_HOST,
        "--port",
        str(settings.BACKEND_PORT)
    ])

    print("[Launcher] Waiting for backend to initialize...")
    time.sleep(3)

    frontend_script = str(BASE_DIR / "frontend" / "app.py")
    print(f"\n[Launcher] Launching Streamlit frontend at http://localhost:{settings.FRONTEND_PORT}...")
    print(f"[Launcher] Swagger API Documentation available at http://{settings.BACKEND_HOST}:{settings.BACKEND_PORT}/docs\n")

    frontend_proc = subprocess.Popen([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        frontend_script,
        "--server.port",
        str(settings.FRONTEND_PORT),
        "--server.headless",
        "true"
    ])

    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\n[Launcher] Shutting down servers...")
        backend_proc.terminate()
        frontend_proc.terminate()
        print("[Launcher] Shutdown complete.")

def main():
    parser = argparse.ArgumentParser(description="ApexFit AI - Master Runner")
    parser.add_argument("--backend", action="store_true", help="Run only the FastAPI backend")
    parser.add_argument("--frontend", action="store_true", help="Run only the Streamlit frontend")
    parser.add_argument("--ingest", action="store_true", help="Force re-ingest fitness knowledge into ChromaDB")
    args = parser.parse_args()

    if args.ingest:
        print("[Launcher] Ingesting fitness knowledge into ChromaDB...")
        ingest_fitness_knowledge(force=True)
        return

    if args.backend:
        banner()
        ingest_fitness_knowledge()
        run_backend()
    elif args.frontend:
        banner()
        run_frontend()
    else:
        run_both()

if __name__ == "__main__":
    main()
