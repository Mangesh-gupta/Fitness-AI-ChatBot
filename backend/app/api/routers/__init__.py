from backend.app.api.routers.auth_router import router as auth_router
from backend.app.api.routers.profile_router import router as profile_router
from backend.app.api.routers.sessions_router import router as sessions_router
from backend.app.api.routers.chat_router import router as chat_router
from backend.app.api.routers.products_router import router as products_router

__all__ = ["auth_router", "profile_router", "sessions_router", "chat_router", "products_router"]
