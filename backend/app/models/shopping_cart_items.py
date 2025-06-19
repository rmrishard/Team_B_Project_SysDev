import uuid
import datetime
from typing import Optional
from pydantic import ConfigDict, AliasChoices
from sqlmodel import Field, SQLModel

class ShoppingCartItemBase(SQLModel):
    __tablename__ = "shopping_cart_item"
    model_config = ConfigDict(extra='ignore')

    shopping_cart_id_fk: uuid.UUID = Field(alias='shopping_cart_id', schema_extra={'serialization_alias': 'shopping_cart_id'})
    product_id_fk: uuid.UUID = Field(alias='product_id', schema_extra={'serialization_alias': 'product_id'})
    added_time: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    reserved: bool = Field(default=False)
    quantity: int = Field(default=0)

class ShoppingCartItem(ShoppingCartItemBase, table=True):
    shopping_cart_item_id_pk: uuid.UUID = Field(alias='id', primary_key=True, default_factory=uuid.uuid4, index=True,
                                               schema_extra={'serialization_alias': 'id'})

    @classmethod
    def getIdField(cls):
        return cls.shopping_cart_item_id_pk

    @classmethod
    def getName(cls):
        return "ShoppingCartItem"

class ShoppingCartItemCreate(ShoppingCartItemBase):
    shopping_cart_id_fk: uuid.UUID = Field(schema_extra={'serialization_alias': 'shopping_cart_id',
                                                         'validation_alias': AliasChoices('shopping_cart_id')})
    product_id_fk: uuid.UUID = Field(schema_extra={'serialization_alias': 'product_id',
                                                  'validation_alias': AliasChoices('product_id')})

class ShoppingCartItemPublic(ShoppingCartItemBase):
    shopping_cart_item_id_pk: uuid.UUID = Field(alias='id', primary_key=True, default_factory=uuid.uuid4, index=True,
                                               schema_extra={'serialization_alias': 'id'})

class ShoppingCartItemPublicRetrieve(ShoppingCartItemPublic):
    model_config = ConfigDict(extra='ignore')

class ShoppingCartItemUpdate(ShoppingCartItemBase):
    model_config = ConfigDict(extra='forbid')
    shopping_cart_item_id_pk: None = Field(default=None, alias='id', index=True, schema_extra={'serialization_alias': 'id'})
    shopping_cart_id_fk: None = Field(default=None, alias='shopping_cart_id')
    product_id_fk: None = Field(default=None, alias='product_id')
    added_time: Optional[datetime.datetime] = None
    reserved: Optional[bool] = None
    quantity: Optional[int] = None