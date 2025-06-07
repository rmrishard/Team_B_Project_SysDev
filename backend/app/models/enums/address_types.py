from typing import Optional, Annotated
from pydantic import ConfigDict, AliasChoices
from sqlmodel import Field, SQLModel

from . import EnumsRegistered
from .enum_type_base import EnumTypeBase

class AddressType(EnumTypeBase, table=True):
    __tablename__ = 'address_type'
    address_type_id_pk: int = Field(alias='id', primary_key=True, index=True, schema_extra={'serialization_alias': 'id'})

    # This allows for helper functions to retrieve the appropriate id field
    @classmethod
    def getIdField(cls):
        return cls.address_type_id_pk #Simply return field used as id

class AddressTypeCreate(EnumTypeBase):
    address_type_id_pk: Optional[Annotated[ int,Field( schema_extra={'serialization_alias': 'id','validation_alias':AliasChoices('id')})]] = None
    pass

class AddressTypePublic(EnumTypeBase):
    address_type_id_pk: int = Field(alias='id', primary_key=True, index=True, schema_extra={'serialization_alias': 'id'})
    pass

class AddressTypeUpdate(EnumTypeBase):
    pass

# Register this enum type in __init__.py
EnumsRegistered["address_types"] = AddressType
