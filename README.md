# 🏋️‍♂️ Fitness AI Chatbot — Intelligent Health & Recommendation System

An enterprise-grade, full-stack AI fitness coaching and product recommendation platform powered by **FastAPI**, **Streamlit**, **LangChain**, **ChromaDB**, **SQLite**, and the **NVIDIA Nemotron 3 Ultra 550B** reasoning model.

---

## 🌟 Key Features

1. **AI-Powered Personalized Coaching**:
   - Science-backed workout programming (PPL, Upper/Lower, Full Body, Calisthenics).
   - Precision macronutrient and calorie deficit/surplus calculations.
   - Evidence-based sports supplementation guidelines.

2. **ChromaDB RAG (Retrieval-Augmented Generation)**:
   - High-density vector store populated with authoritative exercise science, biomechanics, recovery, and nutrition data.
   - Vector similarity search ensures factual, non-hallucinatory guidance.

3. **Transparent AI Reasoning**:
   - Integrates `nvidia/nemotron-3-ultra-550b-a55b` with `enable_thinking=True`.
   - Surfaces model reasoning inside an expandable "🧠 Coach Thinking Process" drawer in real-time.

4. **Dynamic Product Recommendation Engine**:
   - Analyzes real-time user queries and biometrics.
   - Recommends tailored fitness equipment, supplements, and wearables (e.g., knee sleeves for squatting discomfort, Creapure creatine for strength, lifting straps for deadlifts).

5. **FastAPI Backend & JWT Authentication**:
   - Secure registration, password hashing (`bcrypt`), and Bearer JWT token lifecycle.
   - Biometric profile management with automatic **BMI**, **BMR** (Mifflin-St Jeor), and **TDEE** computation.

6. **SQLite Multi-Session Memory**:
   - Full conversational memory preserved per user session.
   - Supports creating, renaming, switching, and deleting consultation threads.

7. **Modern Athletic Streamlit Frontend**:
   - Dark athletic aesthetic with neon accents.
   - Live streaming response generation.
   - Biometric stats drawer and interactive product cards.

---

## 📁 Project Architecture

```
Fitness-AI ChatBot/
├── .env                              # Environment configuration (API keys & settings)
├── requirements.txt                  # Python dependencies

├── run.py                            # Master runner script
├── README.md                         # Project documentation
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py                 # Pydantic environment configuration
│   │   ├── database.py               # SQLite engine and session factory
│   │   ├── main.py                   # FastAPI application entrypoint
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── models.py             # SQLAlchemy models (User, Profile, Session, Message)
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py            # Pydantic request/response schemas
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── security.py           # Bcrypt hashing & JWT management
│   │   │   └── deps.py               # Current user dependency
│   │   ├── rag/
│   │   │   ├── __init__.py
│   │   │   ├── knowledge_data.py     # Authoritative fitness knowledge base
│   │   │   ├── vectorstore.py        # ChromaDB persistent vector store
│   │   │   └── ingest.py             # Ingestion & indexing script
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── llm_service.py        # NVIDIA NIM Nemotron client & prompt chaining
│   │   │   ├── product_service.py    # Contextual product recommendation engine
│   │   │   └── chat_service.py       # Chat turn orchestration & memory persistence
│   │   └── api/
│   │       ├── __init__.py
│   │       └── routers/
│   │           ├── __init__.py
│   │           ├── auth_router.py    # /api/auth (register, login, me)
│   │           ├── profile_router.py # /api/profile (biometrics & BMI/BMR)
│   │           ├── sessions_router.py# /api/sessions (multi-session history)
│   │           ├── chat_router.py    # /api/chat (SSE streaming & JSON)
│   │           └── products_router.py# /api/products (catalog & recommendations)
│   └── data/
│       └── products.json             # Fitness equipment & supplement catalog
└── frontend/
    ├── app.py                        # Streamlit application
    ├── api_client.py                 # REST API client wrapper
    └── components/
        ├── __init__.py
        └── ui.py                     # Custom CSS, product cards, thinking box, sources
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10 or 3.11 installed.

### 2. Configuration (.env)
Create a `.env` file in the project root:
```env
NVIDIA_API_KEY=your_nvidia_api_key_here
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
LLM_MODEL=nvidia/nemotron-3-ultra-550b-a55b
JWT_SECRET_KEY=fitness_ai_super_secret_jwt_key_change_in_production_2026
```



### 3. Launching the Application
You can run both the FastAPI backend and the Streamlit frontend with a single command:

```powershell
python run.py
```

This will automatically:
1. Initialize the SQLite database (`fitness_ai.db`).
2. Populate ChromaDB with curated fitness science documents.
3. Start the FastAPI backend at `http://127.0.0.1:8000`.
4. Launch the Streamlit frontend at `http://localhost:8501`.

### 4. Running Components Separately
- **Only Backend**:
  ```powershell
  python run.py --backend
  ```
  Interactive API Docs: `http://127.0.0.1:8000/docs`

- **Only Frontend**:
  ```powershell
  python run.py --frontend
  ```

---

## 📡 API Endpoints Overview

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/register` | Register new user and initialize profile |
| `POST` | `/api/auth/login` | Log in and receive JWT access token |
| `GET` | `/api/auth/me` | Fetch authenticated user data |
| `GET` | `/api/profile` | Get user biometric profile + computed BMI, BMR, TDEE |
| `PUT` | `/api/profile` | Update user height, weight, goal, activity, diet |
| `GET` | `/api/sessions` | List all consultation sessions for user |
| `POST` | `/api/sessions` | Create a new consultation session |
| `GET` | `/api/sessions/{id}` | Get full conversation history with sources & products |
| `DELETE` | `/api/sessions/{id}` | Delete a consultation thread |
| `POST` | `/api/chat` | Send prompt to AI coach (supports streaming SSE) |
| `GET` | `/api/products` | Browse catalog of fitness supplements & gear |
| `GET` | `/api/products/recommend` | Dynamic query-based product matching |

---

## 💡 Example Queries to Test
1. **Hypertrophy**: *"Can you build a 4-day Upper/Lower split focused on chest and lats?"*
2. **Fat Loss & Diet**: *"I am 82kg and 178cm. Calculate my caloric deficit and macros for fat loss."*
3. **Supplements**: *"What is the optimal dosing protocol and scientific rationale for Creatine?"*
4. **Injury & Gear**: *"My knees ache when I squat below parallel. What can I do and what gear helps?"*
