import uuid
from typing import TypedDict, Optional, Any
from decimal import Decimal

from pydantic import ConfigDict, SkipValidation
from sqlalchemy.dialects.postgresql.psycopg import JSONB
from sqlmodel import Field, SQLModel

# if referring to other models within this model (example)
# if TYPE_CHECKING:
#    from .team_model import Team

class ProductDetail(TypedDict, total=False):
    volume: str # All fields are optional given that total=False
    type: str
    certification: str
    arabic_text: str

# We create a base since this field MUST be present
class ImageDetailBase(TypedDict):
    url: str

# These are optional given that total=False
class ImageDetail(ImageDetailBase, total=False):
    label: str
    width: int
    height: int

class ProductBase(SQLModel):
    model_config = ConfigDict(extra='ignore')
    name: str
    description: str
    price: Decimal
    category: Optional[str] = Field(default=None)
    available: Optional[bool] = Field(default=True)
    visible: Optional[bool] = Field(default=False)
    weight: Optional[Decimal] = Field(default=None)
    dimensions: Optional[str] = Field(default=None)
    stock_quantity: int = Field(default=0)
    image: list[ImageDetail] | None = Field(sa_type=JSONB, nullable=False)
    origin: str | None = Field(default=None)
    details: ProductDetail | None  = Field(sa_type=JSONB, nullable=False)

#When table=True validation is not done, thus it must be done manually
class Product(ProductBase, table=True):
    product_id_pk: uuid.UUID = Field(alias='id', primary_key=True, default_factory=uuid.uuid4, index=True,schema_extra={'serialization_alias': 'id'})

    # REQUIRED: This allows for helper functions to retrieve the appropriate id field
    @classmethod
    def getIdField(cls):
        return cls.product_id_pk

    # REQUIRED: This allows for helper functions to retrieve the appropriate human-name for the entity
    @classmethod
    def getName(cls):
        return "Product"

class ProductCreate(ProductBase):
    pass

class ProductPublic(ProductBase):
    product_id_pk: uuid.UUID = Field(alias='id', primary_key=True, default_factory=uuid.uuid4, index=True,schema_extra={'serialization_alias': 'id'})

# Use this model when retrieving for public consumption
class ProductPublicRetrieve(ProductPublic):
    model_config = ConfigDict(extra='ignore')
    image: SkipValidation[Any] #We don't enforce checks on JSONB schema on retrieve... only insert
    details: SkipValidation[Any] #We don't enforce checks on JSONB schema on retrieve... only insert

#Use this model for updating a model in the database
class ProductUpdate(ProductBase):
    model_config = ConfigDict(extra='forbid')
    product_id_pk: None = Field(default=None, alias='id',schema_extra={'serialization_alias': 'id'}) # DON'T ALLOW PATCHES TO UPDATE PRIMARY KEY!!!
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    available: Optional[bool] = None
    visible: Optional[bool] = None
    weight: Optional[Decimal] = None
    dimensions: Optional[str] = None
    stock_quantity: Optional[int] = None
    image: list[ImageDetail] | None = Field(sa_type=JSONB, default=None)
    origin: Optional[str] = None
    details: ProductDetail | None = Field(sa_type=JSONB, default=None)
