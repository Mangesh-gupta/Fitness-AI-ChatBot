import json
from datetime import datetime
from typing import List, Dict, Any, Generator, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend.app.models.models import User, ChatSession, ChatMessage, UserProfile
from backend.app.schemas.schemas import (
    ChatMessageOut,
    ChatResponse,
    ProductItem,
    SourceItem
)
from backend.app.rag.vectorstore import query_knowledge_base
from backend.app.services.product_service import product_service
from backend.app.services.llm_service import llm_service

class ChatService:
    def get_or_create_session(self, db: Session, user: User, session_id: Optional[str] = None, title: Optional[str] = None) -> ChatSession:
        if session_id:
            session = db.query(ChatSession).filter(
                ChatSession.id == session_id,
                ChatSession.user_id == user.id
            ).first()
            if not session:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
            return session
        
        # Create new session
        new_session = ChatSession(
            user_id=user.id,
            title=title or "New Fitness Consultation"
        )
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        return new_session

    def process_chat_message(
        self,
        db: Session,
        user: User,
        session_id: str,
        user_prompt: str
    ) -> ChatResponse:
        """Non-streaming chat handling with RAG, dynamic products, and conversation memory"""
        session = self.get_or_create_session(db, user, session_id)

        # 1. Save user message to database
        user_msg = ChatMessage(
            session_id=session.id,
            role="user",
            content=user_prompt
        )
        db.add(user_msg)
        db.commit()
        db.refresh(user_msg)

        # 2. Retrieve user profile
        profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
        profile_dict = {
            "age": profile.age if profile else None,
            "gender": profile.gender if profile else None,
            "height_cm": profile.height_cm if profile else None,
            "weight_kg": profile.weight_kg if profile else None,
            "fitness_goal": profile.fitness_goal if profile else "muscle_gain",
            "activity_level": profile.activity_level if profile else "moderate",
            "dietary_preference": profile.dietary_preference if profile else "none",
            "injuries_limitations": profile.injuries_limitations if profile else None
        }

        # 3. Retrieve RAG context from ChromaDB
        rag_results = query_knowledge_base(user_prompt, n_results=3)

        # 4. Build conversation history (last 10 messages)
        past_messages = db.query(ChatMessage).filter(
            ChatMessage.session_id == session.id,
            ChatMessage.id != user_msg.id
        ).order_by(ChatMessage.created_at.asc()).all()[-10:]

        conversation_history = []
        for msg in past_messages:
            conversation_history.append({"role": msg.role, "content": msg.content})
        conversation_history.append({"role": "user", "content": user_prompt})

        # 5. Build prompt & generate response
        system_prompt = llm_service.build_system_prompt(
            user_profile=profile_dict,
            rag_contexts=rag_results
        )

        llm_result = llm_service.generate_response(
            messages=conversation_history,
            system_prompt=system_prompt
        )

        content = llm_result["content"]
        reasoning = llm_result.get("reasoning_content", "")

        # 6. Persist assistant message with sources
        sources_json = json.dumps(rag_results) if rag_results else None

        asst_msg = ChatMessage(
            session_id=session.id,
            role="assistant",
            content=content,
            reasoning_content=reasoning,
            sources_json=sources_json,
            products_json=None
        )

        db.add(asst_msg)

        # Auto-update session title if it's the first exchange
        if session.title == "New Fitness Consultation":
            # Generate short title from prompt
            session.title = user_prompt[:40] + ("..." if len(user_prompt) > 40 else "")

        session.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(asst_msg)

        # Build response objects
        source_items = [SourceItem(**s) for s in rag_results] if rag_results else []
        prod_items = recommended_products

        user_out = ChatMessageOut(
            id=user_msg.id,
            session_id=user_msg.session_id,
            role=user_msg.role,
            content=user_msg.content,
            created_at=user_msg.created_at
        )

        asst_out = ChatMessageOut(
            id=asst_msg.id,
            session_id=asst_msg.session_id,
            role=asst_msg.role,
            content=asst_msg.content,
            reasoning_content=asst_msg.reasoning_content,
            sources=source_items,
            products=prod_items,
            created_at=asst_msg.created_at
        )

        return ChatResponse(
            session_id=session.id,
            user_message=user_out,
            assistant_message=asst_out
        )

    def process_chat_message_stream(
        self,
        db: Session,
        user: User,
        session_id: str,
        user_prompt: str
    ) -> Generator[str, None, None]:
        """Streaming chat handling yielding SSE data formatted chunks"""
        session = self.get_or_create_session(db, user, session_id)

        # Save user message
        user_msg = ChatMessage(
            session_id=session.id,
            role="user",
            content=user_prompt
        )
        db.add(user_msg)
        db.commit()
        db.refresh(user_msg)

        # Retrieve profile
        profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
        profile_dict = {
            "age": profile.age if profile else None,
            "gender": profile.gender if profile else None,
            "height_cm": profile.height_cm if profile else None,
            "weight_kg": profile.weight_kg if profile else None,
            "fitness_goal": profile.fitness_goal if profile else "muscle_gain",
            "activity_level": profile.activity_level if profile else "moderate",
            "dietary_preference": profile.dietary_preference if profile else "none",
            "injuries_limitations": profile.injuries_limitations if profile else None
        }

        # Retrieve RAG context
        rag_results = query_knowledge_base(user_prompt, n_results=3)

        # First SSE events: send metadata (sources)
        meta_event = {
            "event": "meta",
            "sources": rag_results
        }
        yield f"data: {json.dumps(meta_event)}\n\n"

        # Conversation history
        past_messages = db.query(ChatMessage).filter(
            ChatMessage.session_id == session.id,
            ChatMessage.id != user_msg.id
        ).order_by(ChatMessage.created_at.asc()).all()[-10:]

        conversation_history = []
        for msg in past_messages:
            conversation_history.append({"role": msg.role, "content": msg.content})
        conversation_history.append({"role": "user", "content": user_prompt})

        # Build prompt
        system_prompt = llm_service.build_system_prompt(
            user_profile=profile_dict,
            rag_contexts=rag_results
        )

        full_content = []
        full_reasoning = []

        for chunk in llm_service.stream_response(conversation_history, system_prompt):
            chunk_type = chunk["type"]
            text = chunk["text"]
            if chunk_type == "thinking":
                full_reasoning.append(text)
            else:
                full_content.append(text)

            payload = {"event": chunk_type, "text": text}
            yield f"data: {json.dumps(payload)}\n\n"

        # Safely save assistant message to DB after stream completion
        complete_content = "".join(full_content)
        complete_reasoning = "".join(full_reasoning) if full_reasoning else None
        sources_json = json.dumps(rag_results) if rag_results else None

        from backend.app.database import SessionLocal
        save_db = SessionLocal()
        msg_id = None
        try:
            asst_msg = ChatMessage(
                session_id=session.id,
                role="assistant",
                content=complete_content,
                reasoning_content=complete_reasoning,
                sources_json=sources_json,
                products_json=None
            )
            save_db.add(asst_msg)


            curr_session = save_db.query(ChatSession).filter(ChatSession.id == session.id).first()
            if curr_session:
                if curr_session.title in ["New Fitness Consultation", "New Consultation"]:
                    curr_session.title = user_prompt[:40] + ("..." if len(user_prompt) > 40 else "")
                curr_session.updated_at = datetime.utcnow()

            save_db.commit()
            msg_id = asst_msg.id
        except Exception as e:
            save_db.rollback()
            print(f"[ChatService] Error persisting streamed message: {e}")
        finally:
            save_db.close()


        # Send completion event
        done_event = {"event": "done", "message_id": msg_id}
        yield f"data: {json.dumps(done_event)}\n\n"


chat_service = ChatService()
