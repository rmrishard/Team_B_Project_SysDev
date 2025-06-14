from typing import Optional, Sequence, List
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, select, update
from .mocking.products import fake_products as mock_products
from ..models.products import *
from app import engine # works when deployed false error reported by PyCharm IDE
from app.utils.orm import ReadItems, UpdateItems

#Example modified from FastAPI example for APIRouter
router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[ProductPublicRetrieve])
async def read_items(offset: int = 0, limit: int = Query(default=20, le=100)):
    select_modifier = lambda sel: sel.offset(offset).limit(limit)   #Adds pagination support
    items = ReadItems.read(Product, modifier_fn=select_modifier)

    if not items:
        raise HTTPException(status_code=404, detail="No products found")

    return items

@router.get("/{item_id}", response_model=ProductPublicRetrieve)
async def read_item(item_id: uuid.UUID):
    item = ReadItems.with_id(Product, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return item

@router.patch("/{item_id}", response_model=ProductPublicRetrieve)
def update_item(item_id: uuid.UUID, item: ProductUpdate):
    updated_item = UpdateItems.with_id(Product, item, item_id)
    return updated_item

@router.post("/upload/", response_model=List[ProductPublicRetrieve])
def create_items(products: List[ProductCreate]):
    with Session(engine) as session:
        for product in products:
            # Exclude unset to the let the DB determine defaults
            product_data = product.model_dump(exclude_unset=True)
            valid_product = Product.model_validate(product_data)
            session.add(valid_product)
        session.commit()

    return products