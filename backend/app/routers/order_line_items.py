from typing import List
import uuid
from fastapi import APIRouter, HTTPException
from sqlmodel import Session
from app import engine
from .mocking.order_line_items import fake_order_line_items as mock_items
from ..models.order_line_items import *
from app.utils.orm import ReadItems

router = APIRouter(
    prefix="/order_line_items",
    tags=["order_line_items"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[OrderLineItemPublic])
async def read_items():
    items = ReadItems.read(OrderLineItem)
    if not items:
        raise HTTPException(status_code=404, detail="No order line items found")
    return items

@router.get("/{item_id}", response_model=OrderLineItemPublic)
async def read_item(item_id: uuid.UUID):
    item = ReadItems.with_id(OrderLineItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Order line item not found")
    return item

@router.post("/upload/", response_model=List[OrderLineItemPublic])
def create_items(order_line_items: List[OrderLineItemCreate]):
    with Session(engine) as session:
        for item in order_line_items:
            valid_item = OrderLineItem.model_validate(item)
            session.add(valid_item)
        session.commit()
    return order_line_items
