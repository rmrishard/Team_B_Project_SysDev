import datetime
import uuid

from typing import Optional, Annotated, TYPE_CHECKING, TypedDict, List
from pydantic import ConfigDict, AliasChoices, BaseModel
from sqlmodel import Field

# Import models
if TYPE_CHECKING:
    from app.models.products import ImageDetail

class ShoppingCartItemStub(TypedDict):
    shopping_cart_item_id: uuid.UUID
    product_id: uuid.UUID
    quantity: int

class ProductStub(TypedDict):
    product_id: uuid.UUID
    image: list["ImageDetail"]
    description: str

class Cart(BaseModel):
    model_config = ConfigDict(extra='ignore')
    shopping_cart_id: uuid.UUID
    cart_items: Optional[List[ShoppingCartItemStub]] = None
    cart_products: Optional[List[ProductStub]] = None
    guest_token: Optional[str] = None

class CartCreate(Cart):
    model_config = ConfigDict(extra='ignore')
    pass

class CartPublic(Cart):
    pass

class CartUpdate(Cart):
    pass





