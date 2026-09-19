from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException, status
from backend.app.schemas.schemas import ProductItem
from backend.app.services.product_service import product_service

router = APIRouter(prefix="/products", tags=["Fitness Products"])

@router.get("", response_model=List[ProductItem])
def list_products():
    """Browse all fitness supplements, gear, and tech products"""
    products = product_service.get_all()
    return [
        ProductItem(
            id=p["id"],
            name=p["name"],
            category=p["category"],
            description=p["description"],
            price=p["price"],
            currency=p.get("currency", "USD"),
            rating=p["rating"],
            reviews_count=p["reviews_count"],
            image_url=p["image_url"],
            product_url=p["product_url"],
            recommendation_reason="Catalog item"
        )
        for p in products
    ]

@router.get("/recommend", response_model=List[ProductItem])
def recommend_products(
    q: str = Query(..., description="User query or keywords"),
    goal: Optional[str] = Query(None, description="User fitness goal"),
    top_k: int = Query(3, ge=1, le=10)
):
    """Dynamically recommend products matching query context and fitness goal"""
    return product_service.recommend_products(query=q, user_goal=goal, top_k=top_k)

@router.get("/{product_id}", response_model=ProductItem)
def get_product(product_id: str):
    """Retrieve details for a specific fitness product"""
    prod = product_service.get_by_id(product_id)
    if not prod:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return ProductItem(
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
        recommendation_reason="Direct lookup"
    )
