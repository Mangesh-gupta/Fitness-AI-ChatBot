from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# ==================== User & Auth Schemas ====================

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username_or_email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    username: str
    email: str

class UserOut(BaseModel):
    id: str
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

# ==================== User Profile Schemas ====================

class ProfileUpdate(BaseModel):
    age: Optional[int] = Field(None, ge=10, le=120)
    gender: Optional[str] = "male"  # male, female, other
    height_cm: Optional[float] = Field(None, ge=50, le=260)
    weight_kg: Optional[float] = Field(None, ge=20, le=400)
    target_weight_kg: Optional[float] = Field(None, ge=20, le=400)
    fitness_goal: Optional[str] = "muscle_gain"  # muscle_gain, fat_loss, endurance, general_fitness
    activity_level: Optional[str] = "moderate"   # sedentary, light, moderate, very_active
    dietary_preference: Optional[str] = "none"  # none, vegan, vegetarian, keto, paleo, pescatarian
    injuries_limitations: Optional[str] = None

class ProfileOut(ProfileUpdate):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    # Calculated metrics
    bmi: Optional[float] = None
    bmi_category: Optional[str] = None
    bmr: Optional[float] = None
    tdee: Optional[float] = None

    class Config:
        from_attributes = True

# ==================== Product Schemas ====================

class ProductItem(BaseModel):
    id: str
    name: str
    category: str
    description: str
    price: float
    currency: str = "USD"
    rating: float
    reviews_count: int
    image_url: str
    product_url: str
    recommendation_reason: Optional[str] = None

# ==================== Chat & Session Schemas ====================

class SourceItem(BaseModel):
    title: str
    category: str
    snippet: str
    score: Optional[float] = None

class ChatMessageOut(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    reasoning_content: Optional[str] = None
    sources: Optional[List[SourceItem]] = None
    products: Optional[List[ProductItem]] = None
    created_at: datetime

    class Config:
        from_attributes = True

class SessionCreate(BaseModel):
    title: Optional[str] = "New Fitness Consultation"

class SessionUpdate(BaseModel):
    title: str

class SessionOut(BaseModel):
    id: str
    user_id: str
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SessionDetailOut(SessionOut):
    messages: List[ChatMessageOut] = []

class ChatRequest(BaseModel):
    session_id: str
    message: str = Field(..., min_length=1)
    stream: bool = False

class ChatResponse(BaseModel):
    session_id: str
    user_message: ChatMessageOut
    assistant_message: ChatMessageOut
