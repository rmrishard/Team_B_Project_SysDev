from typing import List
import uuid
from fastapi import APIRouter, HTTPException
from sqlmodel import Session
from app import engine
from .mocking.shopping_cart_items import fake_shopping_cart_items as mock_items
from ..models.shopping_cart_items import *
from app.utils.orm import ReadItems, UpdateItems

router = APIRouter(
    prefix="/shopping_cart_items",
    tags=["shopping_cart_items"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[ShoppingCartItemPublicRetrieve])
async def read_items():
    items = ReadItems.read(ShoppingCartItem)
    if not items:
        raise HTTPException(status_code=404, detail="No shopping cart items found")
    return items

@router.get("/{item_id}", response_model=ShoppingCartItemPublicRetrieve)
async def read_item(item_id: uuid.UUID):
    item = ReadItems.with_id(ShoppingCartItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Shopping cart item not found")
    return item

@router.patch("/{item_id}", response_model=ShoppingCartItemPublicRetrieve)
def update_item(item_id: uuid.UUID, item: ShoppingCartItemUpdate):
    updated_item = UpdateItems.with_id(ShoppingCartItem, item, item_id)
    return updated_item

@router.post("/upload/", response_model=List[ShoppingCartItemPublicRetrieve])
def create_items(cart_items: List[ShoppingCartItemCreate]):
    with Session(engine) as session:
        for item in cart_items:
            valid_item = ShoppingCartItem.model_validate(item)
            session.add(valid_item)
        session.commit()
    return cart_items