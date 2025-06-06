from typing import Optional, Sequence, List
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from app import engine # works when deployed false error reported by PyCharm IDE

from .mocking.supplier_products import fake_supplier_products as mock_items
from ..models.supplier_products import *

from app.utils.orm import ReadItems


#Example modified from FastAPI example for APIRouter
router = APIRouter(
    prefix="/supplier_products",
    tags=["supplier_products"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[SupplierProductPublic])
async def read_items():
    items = ReadItems.read(SupplierProduct)

    if not items:
        raise HTTPException(status_code=404, detail="No supplier products found")

    return items


@router.get("/{item_id}")
async def read_item(item_id: uuid.UUID):
    item = ReadItems.with_id(SupplierProduct, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Suppler product not found")

    return item

@router.post("/upload/")
def create_items(supplier_products: List[SupplierProductCreate]):
    with Session(engine) as session:
        for item in supplier_products:
            valid_item = SupplierProduct.model_validate(item)
            session.add(valid_item)
        session.commit()

    return supplier_products