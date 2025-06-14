import uuid
import datetime
from pydantic import ConfigDict, AliasChoices
from sqlmodel import Field, SQLModel
from typing import Optional

class ShoppingCartBase(SQLModel):
    __tablename__ = "shopping_cart"
    model_config = ConfigDict(extra='ignore')

    user_id_fk: uuid.UUID = Field(alias='user_id', schema_extra={'serialization_alias': 'user_id'})
    modification_time: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    empty: bool = Field(default=True)

class ShoppingCart(ShoppingCartBase, table=True):
    shopping_cart_id_pk: uuid.UUID = Field(alias='id', primary_key=True, default_factory=uuid.uuid4, index=True,
                                          schema_extra={'serialization_alias': 'id'})

    @classmethod
    def getIdField(cls):
        return cls.shopping_cart_id_pk

class ShoppingCartCreate(ShoppingCartBase):
    user_id_fk: uuid.UUID = Field(schema_extra={'serialization_alias': 'user_id',
                                               'validation_alias': AliasChoices('user_id')})

class ShoppingCartPublic(ShoppingCartBase):
    shopping_cart_id_pk: uuid.UUID = Field(alias='id', primary_key=True, default_factory=uuid.uuid4, index=True,
                                          schema_extra={'serialization_alias': 'id'})

class ShoppingCartUpdate(ShoppingCartBase):
    model_config = ConfigDict(extra='forbid')
    shopping_cart_id_pk: None = Field(default=None, alias='id', index=True, schema_extra={'serialization_alias': 'id'})
    user_id_fk: None = Field(default=None, alias='user_id')
    modification_time: Optional[datetime.datetime] = None
    empty: Optional[bool] = None