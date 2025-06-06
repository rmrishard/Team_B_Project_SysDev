import datetime
import uuid

from typing import Optional
from pydantic import ConfigDict, AliasChoices
from sqlmodel import Field, SQLModel

class SupplierProductBase(SQLModel):
    __tablename__ = "supplier_product"
    model_config = ConfigDict(extra='ignore')
    product_id_fk: uuid.UUID = Field(alias='product_id', schema_extra={'serialization_alias': 'product_id'})
    supplier_id_fk: uuid.UUID = Field(alias='supplier_id', schema_extra={'serialization_alias': 'supplier_id'})
    label: Optional[str]
    note: Optional[str]

# When table=True validation is not done, thus it must be done manually
class SupplierProduct(SupplierProductBase, table=True):
    supplier_product_id_pk: uuid.UUID = Field(alias='id', primary_key=True, default_factory=uuid.uuid4, index=True, schema_extra={'serialization_alias': 'id'})

    # This allows for helper functions to retrieve the appropriate id field
    @classmethod
    def getIdField(cls):
        return cls.supplier_product_id_pk

class SupplierProductCreate(SupplierProductBase):
    model_config = ConfigDict(extra='ignore')
    product_id_fk: uuid.UUID = Field( schema_extra={'validation_alias':AliasChoices('product_id')})
    supplier_id_fk: uuid.UUID = Field( schema_extra={'validation_alias':AliasChoices('supplier_id')})

    pass

class SupplierProductPublic(SupplierProductBase):
    supplier_product_id_pk: uuid.UUID = Field(alias='id', primary_key=True, default_factory=uuid.uuid4, index=True, schema_extra={'serialization_alias': 'id'})

class SupplierProductUpdate(SupplierProductBase):
    pass





