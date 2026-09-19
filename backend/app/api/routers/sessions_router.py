import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.models import User, ChatSession, ChatMessage
from backend.app.schemas.schemas import (
    SessionOut,
    SessionCreate,
    SessionUpdate,
    SessionDetailOut,
    ChatMessageOut,
    SourceItem,
    ProductItem
)
from backend.app.auth.deps import get_current_user

router = APIRouter(prefix="/sessions", tags=["Chat Sessions"])

@router.get("", response_model=List[SessionOut])
def list_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all chat sessions for the current user"""
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id
    ).order_by(ChatSession.updated_at.desc()).all()
    return sessions

@router.post("", response_model=SessionOut, status_code=status.HTTP_201_CREATED)
def create_session(
    session_data: SessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new chat session"""
    new_session = ChatSession(
        user_id=current_user.id,
        title=session_data.title or "New Fitness Consultation"
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@router.get("/{session_id}", response_model=SessionDetailOut)
def get_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get chat session details and message history"""
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    # Format messages
    formatted_messages = []
    for msg in session.messages:
        sources = None
        if msg.sources_json:
            try:
                sources = [SourceItem(**s) for s in json.loads(msg.sources_json)]
            except Exception:
                sources = None

        products = None
        if msg.products_json:
            try:
                products = [ProductItem(**p) for p in json.loads(msg.products_json)]
            except Exception:
                products = None

        formatted_messages.append(ChatMessageOut(
            id=msg.id,
            session_id=msg.session_id,
            role=msg.role,
            content=msg.content,
            reasoning_content=msg.reasoning_content,
            sources=sources,
            products=products,
            created_at=msg.created_at
        ))

    return SessionDetailOut(
        id=session.id,
        user_id=session.user_id,
        title=session.title,
        created_at=session.created_at,
        updated_at=session.updated_at,
        messages=formatted_messages
    )

@router.put("/{session_id}", response_model=SessionOut)
def update_session(
    session_id: str,
    session_data: SessionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Rename a chat session"""
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    session.title = session_data.title
    db.commit()
    db.refresh(session)
    return session

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a chat session and all its messages"""
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    db.delete(session)
    db.commit()
    return None
