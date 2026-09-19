import json
import os
from typing import List, Dict, Any, Optional
from backend.app.config import settings
from backend.app.schemas.schemas import ProductItem

class ProductService:
    def __init__(self):
        self.products: List[Dict[str, Any]] = []
        self._load_products()

    def _load_products(self):
        """Load product catalog from JSON storage (or external API cache)"""
        if os.path.exists(settings.PRODUCTS_FILE):
            try:
                with open(settings.PRODUCTS_FILE, "r", encoding="utf-8") as f:
                    self.products = json.load(f)
            except Exception as e:
                print(f"[ProductService] Error loading products file: {e}")
                self.products = []
        else:
            print(f"[ProductService] Products file not found at {settings.PRODUCTS_FILE}")
            self.products = []

    def get_all(self) -> List[Dict[str, Any]]:
        return self.products

    def get_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        for prod in self.products:
            if prod["id"] == product_id:
                return prod
        return None

    def recommend_products(
        self,
        query: str,
        user_goal: Optional[str] = None,
        top_k: int = 2
    ) -> List[ProductItem]:
        """
        Dynamically recommend fitness products based on user query keywords and fitness goals.
        Simulates an intelligent external product recommendation API.
        """
        query_lower = query.lower()
        scored_products = []

        for prod in self.products:
            score = 0
            reason = "General fitness support"

            # Check direct name match
            if any(term in query_lower for term in prod["name"].lower().split()):
                score += 5

            # Check tags
            for tag in prod.get("tags", []):
                if tag.replace("_", " ") in query_lower or tag in query_lower:
                    score += 4
                    reason = f"Matches your interest in {tag.replace('_', ' ')}"

            # Category check
            if prod["category"].lower() in query_lower:
                score += 3

            # Check user goal alignment
            if user_goal and user_goal in prod.get("target_goals", []):
                score += 2
                if score <= 2:
                    reason = f"Tailored for your goal of {user_goal.replace('_', ' ')}"

            # Contextual heuristics for common queries
            if ("knee" in query_lower or "joint" in query_lower or "squat" in query_lower) and "knee_sleeves" in prod.get("tags", []):
                score += 8
                reason = "Joint warmth and stabilization for squats & knee comfort"
            elif ("deadlift" in query_lower or "grip" in query_lower or "back" in query_lower) and "straps" in prod.get("tags", []):
                score += 7
                reason = "Prevents grip failure so you can overload your back muscles"
            elif ("creatine" in query_lower or "strength" in query_lower or "atp" in query_lower) and "creatine" in prod.get("tags", []):
                score += 8
                reason = "Clinically proven to maximize ATP energy and explosive strength"
            elif ("protein" in query_lower or "shake" in query_lower or "whey" in query_lower or "hypertrophy" in query_lower) and "whey" in prod.get("tags", []):
                score += 8
                reason = "24g fast-absorbing protein to hit your daily muscle-building target"
            elif ("fat loss" in query_lower or "scale" in query_lower or "track" in query_lower or "weight" in query_lower) and "scale" in prod.get("tags", []):
                score += 6
                reason = "Track lean muscle mass vs. body fat percentage accurately"
            elif ("sore" in query_lower or "recovery" in query_lower or "stretching" in query_lower or "foam" in query_lower) and "foam_roller" in prod.get("tags", []):
                score += 7
                reason = "Accelerates post-workout blood flow and relieves muscle tightness"
            elif ("tired" in query_lower or "energy" in query_lower or "pre workout" in query_lower or "focus" in query_lower) and "pre_workout" in prod.get("tags", []):
                score += 7
                reason = "Clinically dosed citrulline and caffeine for high-intensity output"
            elif ("electrolyte" in query_lower or "cramp" in query_lower or "fasting" in query_lower or "keto" in query_lower) and "electrolytes" in prod.get("tags", []):
                score += 7
                reason = "Zero-sugar sodium and potassium balance to prevent fatigue and cramps"

            if score > 0:
                scored_products.append((score, prod, reason))

        # Sort by score descending
        scored_products.sort(key=lambda x: x[0], reverse=True)

        recommendations = []
        for _, prod, reason in scored_products[:top_k]:
            recommendations.append(ProductItem(
                id=prod["id"],
                name=prod["name"],
                category=prod["category"],
                description=prod["description"],
                price=prod["price"],
                currency=prod.get("currency", "USD"),
                rating=prod["rating"],
                reviews_count=prod["reviews_count"],
                image_url=prod["image_url"],
                product_url=prod["product_url"],
                recommendation_reason=reason
            ))

        return recommendations

product_service = ProductService()
