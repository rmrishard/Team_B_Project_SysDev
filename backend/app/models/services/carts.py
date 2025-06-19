from __future__ import annotations
import datetime
import uuid
from enum import Enum, StrEnum

from typing import Optional, Annotated, TYPE_CHECKING, TypedDict, List
from pydantic import ConfigDict, AliasChoices, BaseModel
from sqlmodel import Field, SQLModel, Relationship
from app.models.products import ImageDetail
from app.models.shopping_carts import ShoppingCart

class CartShoppingCartItemStub(SQLModel):
    shopping_cart_item_id: uuid.UUID = Field(
        schema_extra={'validation_alias': AliasChoices('shopping_cart_item_id_pk')})
    product_id: uuid.UUID = Field(foreign_key="product.product_id_pk",
        schema_extra={'validation_alias': AliasChoices('product_id_fk')})
    product: Product | None = Relationship()
    quantity: int

    @classmethod
    def from_ShoppingCartItem(cls, shopping_cart_item: ShoppingCartItem) -> ShoppingCartItemStub:
        return CartShoppingCartItemStub.model_validate(shopping_cart_item.model_dump(include={"shopping_cart_item_id_pk","quantity","product_id_fk"}))

class CartProductStub(BaseModel):
    product_id: uuid.UUID
    #product_name
    image: list[ImageDetail]
    description: str

class Cart(BaseModel):
    model_config = ConfigDict(extra='ignore')
    shopping_cart_id: uuid.UUID = Field(
        schema_extra={'validation_alias': AliasChoices('shopping_cart_id_pk')})
    cart_items: Optional[List[CartShoppingCartItemStub]] = None
    cart_products: Optional[List[CartProductStub]] = None
    guest_token: Optional[str] = None

    @classmethod
    def from_ShoppingCart(cls, shopping_cart: ShoppingCart) -> CartPublic:
        return CartPublic.model_validate(shopping_cart.model_dump(include={"shopping_cart_id_pk"}))

class CartCreate(Cart):
    model_config = ConfigDict(extra='ignore')
    pass

class CartPublic(Cart):
    pass

class CartUpdate(Cart):
    pass

class CartModifyRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    product_id: uuid.UUID
    quantity: int | None





