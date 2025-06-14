from typing import List
import uuid
from fastapi import APIRouter, HTTPException
from sqlmodel import Session
from app import engine
from .mocking.shopping_carts import fake_shopping_carts as mock_items
from ..models.shopping_carts import *
from app.utils.orm import ReadItems, UpdateItems

router = APIRouter(
    prefix="/shopping_carts",
    tags=["shopping_carts"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[ShoppingCartPublic])
async def read_items():
    items = ReadItems.read(ShoppingCart)
    if not items:
        raise HTTPException(status_code=404, detail="No shopping carts found")
    return items

@router.get("/{item_id}", response_model=ShoppingCartPublic)
async def read_item(item_id: uuid.UUID):
    item = ReadItems.with_id(ShoppingCart, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    return item

@router.patch("/{item_id}", response_model=ShoppingCartPublic)
def update_item(item_id: uuid.UUID, item: ShoppingCartUpdate):
    updated_item = UpdateItems.with_id(ShoppingCart, item, item_id)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    return updated_item


@router.post("/upload/", response_model=List[ShoppingCartPublic])
def create_items(shopping_carts: List[ShoppingCartCreate]):
    with Session(engine) as session:
        for item in shopping_carts:
            valid_item = ShoppingCart.model_validate(item)
            session.add(valid_item)
        session.commit()
    return shopping_carts