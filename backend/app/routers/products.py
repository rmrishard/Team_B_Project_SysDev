from typing import Optional, Sequence
from fastapi import APIRouter, HTTPException
from .mocking.products import fake_products as mock_products
from ..models.products import *
from app import engine # works when deployed false error reported by PyCharm IDE

#Example modified from FastAPI example for APIRouter
router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_items()->Sequence[Product]:
    with Session(engine) as session:
        statement = select(Product)
        results = session.exec(statement)
        return results.fetchall()
    #return mock_products


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
            valid_product = Product.model_validate(product)
            session.add(valid_product)
        session.commit()

    return products

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