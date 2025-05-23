from fastapi import APIRouter, HTTPException
from typing import TypedDict
from pydantic import BaseModel, ConfigDict

from .mocking.products import fake_products as mock_products

#Example modified from FastAPI example for APIRouter

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

class ProductDetail(TypedDict, total=False):
    model_config = ConfigDict(extra='ignore')  
    volume: str | None = None
    type: str | None = None
    certification: str | None = None
    arabic_text: str | None = None

class Product(BaseModel):
    model_config = ConfigDict(extra='ignore')  
    id: int
    name: str
    description: str
    price: float
    image: str
    origin: str
    details: ProductDetail

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