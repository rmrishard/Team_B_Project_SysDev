from typing import Optional, Sequence, List
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from app import engine # works when deployed false error reported by PyCharm IDE

from .mocking.supplier_products import fake_supplier_products as mock_items
from ..models.supplier_products import *

#Example modified from FastAPI example for APIRouter
router = APIRouter(
    prefix="/supplier_products",
    tags=["supplier_products"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[SupplierProductPublic])
async def read_items():
    with Session(engine) as session:
        statement = select(SupplierProduct)
        results = session.exec(statement).all()
        return results
    return None


@router.get("/{item_id}")
async def read_item(item_id: int):
    # Do search within logic, move to query for DB server to do later
    matches = list(filter( lambda item: item["id"]==item_id ,mock_items["supplier_products"]))

    if len(matches) == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        #this processing will change when pulling from DB
        supplier_product = SupplierProduct.model_validate(matches[0])
    
    return {"supplier_products":[supplier_product]}

@router.post("/upload/")
def create_items(supplier_products: List[SupplierProductCreate]):
    with Session(engine) as session:
        for item in supplier_products:
            valid_item = SupplierProduct.model_validate(item)
            session.add(valid_item)
        session.commit()

    return supplier_products