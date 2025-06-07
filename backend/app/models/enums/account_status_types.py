from typing import Optional, Annotated
from pydantic import ConfigDict, AliasChoices
from sqlmodel import Field, SQLModel

from . import EnumsRegistered
from .enum_type_base import EnumTypeBase

class AccountStatusType(EnumTypeBase, table=True):
    __tablename__ = 'account_status_type'
    account_status_type_id_pk: int = Field(alias='id', primary_key=True, index=True, schema_extra={'serialization_alias': 'id'})

    # This allows for helper functions to retrieve the appropriate id field
    @classmethod
    def getIdField(cls):
        return cls.account_status_type_id_pk #Simply return field used as id

class AccountStatusTypeCreate(EnumTypeBase):
    account_status_type_id_pk: Optional[Annotated[ int,Field( schema_extra={'serialization_alias': 'id','validation_alias':AliasChoices('id')})]] = None
    pass

class AccountStatusTypePublic(EnumTypeBase):
    account_status_type_id_pk: int = Field(alias='id', primary_key=True, index=True, schema_extra={'serialization_alias': 'id'})
    pass

class AccountStatusTypeUpdate(EnumTypeBase):
    pass

# Register this enum type in __init__.py
EnumsRegistered["account_status_types"] = AccountStatusType
