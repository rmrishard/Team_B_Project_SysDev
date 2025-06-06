import datetime
import uuid

from typing import Optional, Annotated
from pydantic import ConfigDict, AliasChoices
from sqlmodel import Field, SQLModel

class SupplierBase(SQLModel):
    model_config = ConfigDict(extra='ignore')
    address_id_fk: Optional[Annotated[uuid.UUID,Field(alias='address_id', schema_extra={'serialization_alias': 'address_id'})]] = None
    name: str
    phone: str
    email: str

# When table=True validation is not done, thus it must be done manually
class Supplier(SupplierBase, table=True):
    supplier_id_pk: uuid.UUID = Field(alias='id', primary_key=True, default_factory=uuid.uuid4, index=True, schema_extra={'serialization_alias': 'id'})

    # This allows for helper functions to retrieve the appropriate id field
    @classmethod
    def getIdField(cls):
        return cls.supplier_id_pk

class SupplierCreate(SupplierBase):
    model_config = ConfigDict(extra='ignore')
    address_id_fk: Optional[Annotated[ uuid.UUID,Field( schema_extra={'serialization_alias': 'address_id','validation_alias':AliasChoices('address_id')})]] = None

    pass

class SupplierPublic(SupplierBase):
    supplier_id_pk: uuid.UUID = Field(alias='id', primary_key=True, default_factory=uuid.uuid4, index=True, schema_extra={'serialization_alias': 'id'})
    address_id_fk: Optional[uuid.UUID] = Field(default=None, schema_extra={'serialization_alias': 'address_id'})

class SupplierUpdate(SupplierBase):
    pass





