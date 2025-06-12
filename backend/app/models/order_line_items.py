import uuid
from decimal import Decimal
from typing import Optional, TYPE_CHECKING
from pydantic import ConfigDict, AliasChoices
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .orders import Order

class OrderLineItemBase(SQLModel):
    __tablename__ = "order_line_item"
    model_config = ConfigDict(extra='ignore')

    product_id_fk: uuid.UUID = Field(alias='product_id', schema_extra={'serialization_alias': 'product_id'})
    product_name: str
    product_qty: int
    product_price: Decimal
    stock_quantity: int
    order_id_fk: uuid.UUID = Field(alias='order_id', schema_extra={'serialization_alias': 'order_id'})
    line_type_id_fk: int = Field(alias='line_type_id', schema_extra={'serialization_alias': 'line_type_id'})

class OrderLineItem(OrderLineItemBase, table=True):
    order_line_id_pk: uuid.UUID = Field(alias='id', primary_key=True, default_factory=uuid.uuid4, index=True,
                                       schema_extra={'serialization_alias': 'id'})
    #order: Optional["Order"] = Relationship(back_populates="line_items")

    @classmethod
    def getIdField(cls):
        return cls.order_line_id_pk

class OrderLineItemCreate(OrderLineItemBase):
    product_id_fk: uuid.UUID = Field(schema_extra={'serialization_alias': 'product_id',
                                                  'validation_alias': AliasChoices('product_id')})
    order_id_fk: uuid.UUID = Field(schema_extra={'serialization_alias': 'order_id',
                                                'validation_alias': AliasChoices('order_id')})
    line_type_id_fk: int = Field(schema_extra={'serialization_alias': 'line_type_id',
                                              'validation_alias': AliasChoices('line_type_id')})

class OrderLineItemPublic(OrderLineItemBase):
    order_line_id_pk: uuid.UUID = Field(alias='id', primary_key=True, default_factory=uuid.uuid4, index=True,
                                       schema_extra={'serialization_alias': 'id'})

class OrderLineItemPublicRetrieve(OrderLineItemPublic):
    pass

class OrderLineItemUpdate(OrderLineItemBase):
    model_config = ConfigDict(extra='forbid')
    order_line_id_pk: None = Field(default=None, alias='id',index=True, schema_extra={'serialization_alias': 'id'})
    product_id_fk: None = Field(default=None, alias='product_id', schema_extra={'serialization_alias': 'product_id'})
    product_name: Optional[str] = None
    product_qty: Optional[int] = None
    product_price: Optional[Decimal] = None
    stock_quantity: Optional[int] = None
    order_id_fk: None = Field(default=None, alias='order_id', schema_extra={'serialization_alias': 'order_id'})
    line_type_id_fk: None = Field(default=None, alias='line_type_id', schema_extra={'serialization_alias': 'line_type_id'})
