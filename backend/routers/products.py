from fastapi import APIRouter, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

from .mocking.products import fake_products as mock_products
from ..models.products import *

#Example modified from FastAPI example for APIRouter
router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_items():
    return mock_products


@router.get("/{item_id}")
async def read_item(item_id: int):
    #Do search within logic, move to query for DB server to do later
    matches = list(filter( lambda item: item["id"]==item_id ,mock_products["products"]))
    product = None

    if len(matches) == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        #this processing will change when pulling from DB
        product = Product.model_validate(matches[0])
    
    return {"products":[product]}


# @router.put(
#     "/{item_id}",
#     tags=["custom"],
#     responses={403: {"description": "Operation forbidden"}},
# )
# async def update_item(item_id: int):
#     if item_id != "plumbus":
#         raise HTTPException(
#             status_code=403, detail="You can only update the item: plumbus"
#         )
#     return {"item_id": item_id, "name": "The great Plumbus"}