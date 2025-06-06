import datetime
import uuid

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel

class SupplierProductBase(SQLModel):
    __tablename__ = "product_review"
    model_config = ConfigDict(extra='ignore')
    product_id_fk: uuid.UUID = Field(alias='product_id', default_factory=uuid.uuid4)
    supplier_id_fk: uuid.UUID = Field(alias='supplier_id', default_factory=uuid.uuid4)
    label: Optional[str]
    note: Optional[str]

# When table=True validation is not done, thus it must be done manually
class SupplierProduct(SupplierProductBase, table=True):
    supplier_product_id_pk: uuid.UUID = Field(alias='id', primary_key=True, default_factory=uuid.uuid4, index=True)

class SupplierProductCreate(SupplierProductBase):
    pass

class SupplierProductPublic(SupplierProductBase):
    supplier_product_id_pk: uuid.UUID = Field(alias='id', primary_key=True, default_factory=uuid.uuid4, index=True)

class SupplierProductUpdate(SupplierProductBase):
    pass





