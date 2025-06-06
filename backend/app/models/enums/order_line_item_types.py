from typing import Optional, Annotated
from pydantic import ConfigDict, AliasChoices
from sqlmodel import Field, SQLModel

from . import EnumsRegistered
from .enum_type_base import EnumTypeBase

# When table=True validation is not done, thus it must be done manually
class OrderLineItemType(EnumTypeBase, table=True):
    __tablename__ = 'order_line_item_type'
    order_line_item_type_id_pk: int = Field(alias='id', primary_key=True, index=True, schema_extra={'serialization_alias': 'id'})

    # This allows for helper functions to retrieve the appropriate id field
    @classmethod
    def getIdField(cls):
        return cls.order_line_item_type_id_pk #Simply return field used as id

class OrderLineItemTypeCreate(EnumTypeBase):
    order_line_item_type_id_pk: Optional[Annotated[ int,Field( schema_extra={'serialization_alias': 'id','validation_alias':AliasChoices('id')})]] = None
    pass

class OrderLineItemTypePublic(EnumTypeBase):
    order_line_item_type_id_pk: int = Field(alias='id', primary_key=True, index=True, schema_extra={'serialization_alias': 'id'})
    pass

class OrderLineItemTypeUpdate(EnumTypeBase):
    pass

# Register this enum type in __init__.py
EnumsRegistered["ol_item_types"] = OrderLineItemType



