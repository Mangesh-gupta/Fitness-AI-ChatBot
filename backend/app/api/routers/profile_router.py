from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.models import User, UserProfile
from backend.app.schemas.schemas import ProfileUpdate, ProfileOut
from backend.app.auth.deps import get_current_user

router = APIRouter(prefix="/profile", tags=["User Profile"])

def calculate_health_metrics(profile: UserProfile) -> dict:
    """Calculate BMI, BMR, and TDEE based on user profile stats"""
    metrics = {
        "bmi": None,
        "bmi_category": None,
        "bmr": None,
        "tdee": None
    }

    if profile.height_cm and profile.weight_kg and profile.height_cm > 0:
        height_m = profile.height_cm / 100.0
        bmi = round(profile.weight_kg / (height_m ** 2), 1)
        metrics["bmi"] = bmi

        if bmi < 18.5:
            metrics["bmi_category"] = "Underweight"
        elif bmi < 25.0:
            metrics["bmi_category"] = "Normal weight"
        elif bmi < 30.0:
            metrics["bmi_category"] = "Overweight"
        else:
            metrics["bmi_category"] = "Obese"

    if profile.weight_kg and profile.height_cm and profile.age:
        # Mifflin-St Jeor Equation
        gender = (profile.gender or "male").lower()
        if gender == "female":
            bmr = round(10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age - 161, 1)
        else:
            bmr = round(10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age + 5, 1)
        metrics["bmr"] = bmr

        # TDEE Multipliers
        activity_multipliers = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "very_active": 1.725
        }
        mult = activity_multipliers.get(profile.activity_level or "moderate", 1.55)
        metrics["tdee"] = round(bmr * mult, 1)

    return metrics

@router.get("", response_model=ProfileOut)
def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve the current user's profile with calculated biometric stats"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    metrics = calculate_health_metrics(profile)

    return ProfileOut(
        id=profile.id,
        user_id=profile.user_id,
        age=profile.age,
        gender=profile.gender,
        height_cm=profile.height_cm,
        weight_kg=profile.weight_kg,
        target_weight_kg=profile.target_weight_kg,
        fitness_goal=profile.fitness_goal,
        activity_level=profile.activity_level,
        dietary_preference=profile.dietary_preference,
        injuries_limitations=profile.injuries_limitations,
        created_at=profile.created_at,
        updated_at=profile.updated_at,
        **metrics
    )

@router.put("", response_model=ProfileOut)
def update_user_profile(
    profile_update: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user biometric profile & recalculate fitness metrics"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)

    for field, value in profile_update.dict(exclude_unset=True).items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)

    metrics = calculate_health_metrics(profile)

    return ProfileOut(
        id=profile.id,
        user_id=profile.user_id,
        age=profile.age,
        gender=profile.gender,
        height_cm=profile.height_cm,
        weight_kg=profile.weight_kg,
        target_weight_kg=profile.target_weight_kg,
        fitness_goal=profile.fitness_goal,
        activity_level=profile.activity_level,
        dietary_preference=profile.dietary_preference,
        injuries_limitations=profile.injuries_limitations,
        created_at=profile.created_at,
        updated_at=profile.updated_at,
        **metrics
    )
