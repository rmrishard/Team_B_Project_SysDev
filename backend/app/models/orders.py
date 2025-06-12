import datetime
import uuid
from decimal import Decimal
from typing import Optional, List
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel, Relationship
from pydantic import AliasChoices


class OrderBase(SQLModel):
    model_config = ConfigDict(extra='ignore')

    user_id_fk: uuid.UUID = Field(alias='user_id', default_factory=uuid.uuid4,
                                  schema_extra={'serialization_alias': 'user_id'})
    order_status_type_id_fk: int = Field(alias='order_status_type_id',
                                         schema_extra={'serialization_alias': 'order_status_type_id'})
    order_type_id_fk: int = Field(alias='order_type_id', schema_extra={'serialization_alias': 'order_type_id'})
    payment_type_id_fk: int = Field(alias='payment_type_id', schema_extra={'serialization_alias': 'payment_type_id'})
    shipping_address_id_fk: uuid.UUID = Field(alias='shipping_address_id',schema_extra={'serialization_alias': 'shipping_address_id'})
    billing_address_id_fk: uuid.UUID = Field(alias='billing_address_id',schema_extra={'serialization_alias': 'billing_address_id'})
    payment_processed: bool
    special_request: Optional[str] = None
    total_amount: Decimal = 0
    order_date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


class Order(OrderBase, table=True):
    order_id_pk: uuid.UUID = Field(alias='id', primary_key=True, default_factory=uuid.uuid4, index=True,
                                   schema_extra={'serialization_alias': 'id'})
    # line_items: List["OrderLineItem"] = Relationship(back_populates="order")

    @classmethod
    def getIdField(cls):
        return cls.order_id_pk

    @classmethod
    def getName(cls):
        return "Order"


class OrderCreate(OrderBase):
    order_status_type_id_fk : int = Field(
        schema_extra={'serialization_alias': 'order_status_type_id', 'validation_alias': AliasChoices('order_status_type_id')})
    user_id_fk: uuid.UUID = Field(
        schema_extra={'serialization_alias': 'user_id', 'validation_alias': AliasChoices('user_id')})
    order_type_id_fk: int = Field(
        schema_extra={'serialization_alias': 'order_type_id', 'validation_alias': 'order_type_id'})
    payment_type_id_fk: int = Field(
        schema_extra={'serialization_alias': 'payment_type_id', 'validation_alias': 'payment_type_id'})
    shipping_address_id_fk: uuid.UUID = Field(
        schema_extra={'serialization_alias': 'shipping_address_id','validation_alias': 'shipping_address_id'})
    billing_address_id_fk: uuid.UUID = Field(
        schema_extra={'serialization_alias': 'billing_address_id','validation_alias': 'billing_address_id'})





class OrderPublic(OrderBase):
    order_id_pk: uuid.UUID = Field(alias='id', primary_key=True, default_factory=uuid.uuid4, index=True,
                                   schema_extra={'serialization_alias': 'id'})


class OrderPublicRetrieve(OrderPublic):
    model_config = ConfigDict(extra='ignore')



class OrderUpdate(OrderBase):
    model_config = ConfigDict(extra='forbid')
    order_id_pk: None = Field(default=None, alias='id', schema_extra={'serialization_alias': 'id'})
    user_id_fk: Optional[uuid.UUID] = Field(default=None, alias='user_id')
    order_status_type_id_fk: Optional[uuid.UUID] = Field(default=None, alias='order_status_type_id')
    order_type_id_fk: Optional[uuid.UUID] = Field(default=None, alias='order_type_id')
    payment_type_id_fk: Optional[uuid.UUID] = Field(default=None, alias='payment_type_id')
    shipping_address_id_fk: Optional[uuid.UUID] = Field(default=None, alias='shipping_address_id')
    billing_address_id_fk: Optional[uuid.UUID] = Field(default=None, alias='billing_address_id')
    payment_processed: Optional[bool] = None
    special_request: Optional[str] = None
    total_amount: Optional[Decimal] = None
    order_date: Optional[datetime.datetime] = None
