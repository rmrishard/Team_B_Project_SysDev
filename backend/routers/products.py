from fastapi import APIRouter, HTTPException

#Example modified from FastAPI example for APIRouter

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

from pydantic import BaseModel, ConfigDict

class ProductDetail(BaseModel):
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

fake_items_db = {
  "products": [
    {
      "id": 1,
      "name": "El-Koura Extra Virgin Olive Oil",
      "description": "Premium cold-pressed olive oil with no cholesterol. Naturally extracted using traditional methods. Product of Safer region.",
      "price": 34.99,
      "image": "products/olive-oil.jpg",
      "origin": "Lebanon",
      "details": {
        "volume": "3 Liters (101 FL. OZ)",
        "type": "Cold Pressed",
        "certification": "100% Pure Virgin Oil",
        "arabic_text": "الكورة البكر الممتاز"
      }
    },
    {
      "id": 2,
      "name": "Celon Horse Head Starch Tea",
      "description": "Traditional Lebanese starch-based tea blend with distinctive horse head branding. Authentic regional recipe.",
      "price": 14.99,
      "image": "products/Tea.jpeg",
      "origin": "Lebanon",
      "details": {
        "weight": "400g",
        "type": "Herbal Tea Blend",
        "characteristic": "Traditional Preparation",
        "arabic_text": "شاي سيلاني رأس الحصان"
      }
    }
  ]
}

@router.get("/")
async def read_items():
    return fake_items_db


@router.get("/{item_id}")
async def read_item(item_id: int):
    #Do search within logic, move to query for DB server to do later
    matches = list(filter( lambda item: item["id"]==item_id ,fake_items_db["products"]))
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