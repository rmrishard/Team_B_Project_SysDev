from typing import Optional, Sequence, List
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from .mocking.products import fake_products as mock_products
from ..models.products import *
from app import engine # works when deployed false error reported by PyCharm IDE
from app.utils.orm import ReadItems

#Example modified from FastAPI example for APIRouter
router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model=list[ProductPublicRetrieve])
async def read_items():
    items = ReadItems.read(Product)

    if not items:
        raise HTTPException(status_code=404, detail="No products found")

    return items

@router.get("/{item_id}", response_model=ProductPublicRetrieve)
async def read_item(item_id: uuid.UUID):
    item = ReadItems.with_id(Product, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return item[0]

@router.post("/upload/")
def create_items(products: List[ProductCreate]):
    with Session(engine) as session:
        for product in products:
            # Exclude unset to the let the DB determine defaults
            product_data = product.model_dump(exclude_unset=True)
            valid_product = Product.model_validate(product_data)
            session.add(valid_product)
        session.commit()

    return products