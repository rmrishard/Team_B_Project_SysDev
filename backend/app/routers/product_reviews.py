from typing import Optional, Sequence, List
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from .mocking.product_reviews import fake_product_reviews as mock_products
from ..models.product_reviews import *
from app import engine # works when deployed false error reported by PyCharm IDE

#Example modified from FastAPI example for APIRouter
router = APIRouter(
    prefix="/product_reviews",
    tags=["product_reviews"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_items()->Sequence[ProductReview]:
    with Session(engine) as session:
        statement = select(ProductReview)
        results = session.exec(statement)
        return results.fetchall()
    #return mock_products


@router.get("/{item_id}")
async def read_item(item_id: int):
    # Do search within logic, move to query for DB server to do later
    matches = list(filter( lambda item: item["id"]==item_id ,mock_products["product_reviews"]))
    product = None

    if len(matches) == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        #this processing will change when pulling from DB
        product_review = ProductReview.model_validate(matches[0])
    
    return {"product_reviews":[product_review]}

@router.post("/upload/")
def create_items(product_reviews: List[ProductReviewCreate]):
    with Session(engine) as session:
        for item in product_reviews:
            valid_product_review = ProductReview.model_validate(item)
            session.add(valid_product_review)
        session.commit()

    return product_reviews