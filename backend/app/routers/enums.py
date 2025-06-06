from typing import Optional, Sequence, List, Any
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from app import engine # works when deployed false error reported by PyCharm IDE

from ..models.enums import *
from ..models.enums import EnumsRegistered

from app.utils.orm import ReadItems

router = APIRouter(
    prefix="/enums",
    tags=["enums"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{enum_type}", response_model=List[Any])
async def read_items(enum_type: str):
    items = []

    if enum_type not in EnumsRegistered:
        raise HTTPException(status_code=404, detail="Invalid enum type requested")
    else:
        items = ReadItems.read(EnumsRegistered[enum_type])

    return items


@router.get("/{enum_type}/{item_id}")
async def read_item(enum_type: str, item_id: int):
    item = None

    if enum_type not in EnumsRegistered:
        raise HTTPException(status_code=404, detail="Invalid enum type requested")
    else:
        item = ReadItems.with_id(EnumsRegistered[enum_type], item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Enum not found")

    return item

# @router.post("/upload/")
# def create_items(suppliers: List[SupplierCreate]):
#     with Session(engine) as session:
#         for item in suppliers:
#             valid_item = Supplier.model_validate(item)
#             session.add(valid_item)
#         session.commit()
#
#     return suppliers