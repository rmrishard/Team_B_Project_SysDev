from typing import List
import uuid
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session
from app import engine
from .mocking.orders import fake_orders as mock_items
from ..models.orders import *
from app.utils.orm import ReadItems, UpdateItems

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[OrderPublicRetrieve])
async def read_items(offset: int = 0, limit: int = Query(default=20, le=100)):
    select_modifier = lambda sel: sel.offset(offset).limit(limit)
    items = ReadItems.read(Order, modifier_fn=select_modifier)

    if not items:
        raise HTTPException(status_code=404, detail="No orders found")

    return items

@router.get("/{item_id}", response_model=OrderPublicRetrieve)
async def read_item(item_id: uuid.UUID):
    item = ReadItems.with_id(Order, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Order not found")

    return item

@router.patch("/{item_id}", response_model=OrderPublicRetrieve)
def update_item(item_id: uuid.UUID, item: OrderUpdate):
    updated_item = UpdateItems.with_id(Order, item, item_id)
    return updated_item

# @router.get("/{item_id}/total")
# def get_order_total(item_id: uuid.UUID):
#     item = ReadItems.with_id(Order, item_id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Order not found")
#
#     # Recalculate total using the model method
#     item.calculate_total()
#     return float(item.total)

@router.post("/upload/", response_model=List[OrderPublicRetrieve])
def create_items(orders: List[OrderCreate]):
    with Session(engine) as session:
        for order in orders:
            order_data = order.model_dump(exclude_unset=True)
            valid_item = Order.model_validate(order_data)
            session.add(valid_item)
        session.commit()

    return orders
