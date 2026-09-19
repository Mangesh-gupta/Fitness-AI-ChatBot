from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.models import User
from backend.app.schemas.schemas import ChatRequest, ChatResponse
from backend.app.services.chat_service import chat_service
from backend.app.auth.deps import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat & Recommendations"])

@router.post("", response_model=ChatResponse)
def chat_message(
    chat_req: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a message to the AI Fitness Coach.
    Supports non-streaming and streaming (via SSE).
    """
    if chat_req.stream:
        return StreamingResponse(
            chat_service.process_chat_message_stream(
                db=db,
                user=current_user,
                session_id=chat_req.session_id,
                user_prompt=chat_req.message
            ),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )
    else:
        return chat_service.process_chat_message(
            db=db,
            user=current_user,
            session_id=chat_req.session_id,
            user_prompt=chat_req.message
        )
