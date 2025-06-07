from typing import Optional, Annotated
from pydantic import ConfigDict, AliasChoices
from sqlmodel import Field, SQLModel

from . import EnumsRegistered
from .enum_type_base import EnumTypeBase

class UserRoleType(EnumTypeBase, table=True):
    __tablename__ = 'user_role_type'
    user_role_type_id_pk: int = Field(alias='id', primary_key=True, index=True, schema_extra={'serialization_alias': 'id'})

    # This allows for helper functions to retrieve the appropriate id field
    @classmethod
    def getIdField(cls):
        return cls.user_role_type_id_pk #Simply return field used as id

class UserRoleTypeCreate(EnumTypeBase):
    user_role_type_id_pk: Optional[Annotated[ int,Field( schema_extra={'serialization_alias': 'id','validation_alias':AliasChoices('id')})]] = None
    pass

class UserRoleTypePublic(EnumTypeBase):
    user_role_type_id_pk: int = Field(alias='id', primary_key=True, index=True, schema_extra={'serialization_alias': 'id'})
    pass

class UserRoleTypeUpdate(EnumTypeBase):
    pass

# Register this enum type in __init__.py
EnumsRegistered["user_role_types"] = UserRoleType
