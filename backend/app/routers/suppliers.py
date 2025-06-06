from typing import Optional, Sequence, List
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from app import engine # works when deployed false error reported by PyCharm IDE

from .mocking.suppliers import fake_suppliers as mock_items
from ..models.suppliers import *

from app.utils.orm import ReadItems


#Example modified from FastAPI example for APIRouter
router = APIRouter(
    prefix="/suppliers",
    tags=["suppliers"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[SupplierPublic])
async def read_items():
    items = ReadItems.read(Supplier)

    if not items:
        raise HTTPException(status_code=404, detail="No suppliers found")

    return items


@router.get("/{item_id}", response_model=SupplierPublic)
async def read_item(item_id: uuid.UUID):
    item = ReadItems.with_id(Supplier, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Supplier not found")

    return item

@router.post("/upload/", response_model=List[SupplierPublic])
def create_items(suppliers: List[SupplierCreate]):
    with Session(engine) as session:
        for item in suppliers:
            valid_item = Supplier.model_validate(item)
            session.add(valid_item)
        session.commit()

    return suppliers