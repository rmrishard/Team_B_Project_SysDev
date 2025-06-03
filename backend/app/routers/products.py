from typing import Optional, Sequence, List
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from .mocking.products import fake_products as mock_products
from ..models.products import *
from app import engine # works when deployed false error reported by PyCharm IDE

#Example modified from FastAPI example for APIRouter
router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model=list[ProductPublic])
async def read_items():
    with Session(engine) as session:
        statement = select(Product)
        results = session.exec(statement).all()
        return results

@router.get("/{item_id}")
async def read_item(item_id: int):
    # Do search within logic, move to query for DB server to do later
    matches = list(filter( lambda item: item["id"]==item_id ,mock_products["products"]))
    product = None

    if len(matches) == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        #this processing will change when pulling from DB
        product = Product.model_validate(matches[0])
    
    return {"products":[product]}

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