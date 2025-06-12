from typing import Optional, Sequence, List
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from .mocking.product_reviews import fake_product_reviews as mock_product_reviews
from ..models.product_reviews import *
from app import engine # works when deployed false error reported by PyCharm IDE
from app.utils.orm import ReadItems, UpdateItems

#Example modified from FastAPI example for APIRouter
router = APIRouter(
    prefix="/product_reviews",
    tags=["product_reviews"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[ProductReviewPublic])
async def read_items():
    items = ReadItems.read(ProductReview)

    if not items:
        raise HTTPException(status_code=404, detail="No product reviews found")

    return items


@router.get("/{item_id}" , response_model=ProductReviewPublic)
async def read_item(item_id: uuid.UUID):
    item = ReadItems.with_id(ProductReview, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Product review not found")

    return item

@router.patch("/{item_id}", response_model=ProductReviewPublicRetrieve)
def update_item(item_id: uuid.UUID, item: ProductReviewUpdate):
    updated_item = UpdateItems.with_id(ProductReview, item, item_id)
    return updated_item

@router.post("/upload/", response_model=List[ProductReviewPublic])
def create_items(product_reviews: List[ProductReviewCreate]):
    with Session(engine) as session:
        for item in product_reviews:
            valid_product_review = ProductReview.model_validate(item)
            session.add(valid_product_review)
        session.commit()

    return product_reviews