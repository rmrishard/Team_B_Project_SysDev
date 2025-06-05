import uuid
from typing import TypedDict, Optional, Any

from pydantic import ConfigDict, SkipValidation
from sqlalchemy.dialects.postgresql import JSONB
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
    price: float
    weight: Optional[float] = Field(default=None)
    dimensions: Optional[str] = Field(default=None)
    stock_quantity: int = Field(default=0)
    image: list[ImageDetail] | None = Field(sa_type=JSONB, nullable=False)
    origin: str | None = Field(default=None)
    details: ProductDetail | None  = Field(sa_type=JSONB, nullable=False)

#When table=True validation is not done, thus it must be done manually
class Product(ProductBase, table=True):
    id: uuid.UUID = Field(alias='product_id', primary_key=True, default_factory=uuid.uuid4, index=True)

class ProductCreate(ProductBase):
    pass

class ProductPublic(ProductBase):
    id: uuid.UUID = Field(alias='product_id', primary_key=True, default_factory=uuid.uuid4, index=True)

# Use this model when retrieving for public consumption
class ProductPublicRetrieve(ProductPublic):
    model_config = ConfigDict(extra='ignore')
    image: SkipValidation[Any] #We don't enforce checks on JSONB schema on retrieve... only insert
    details: SkipValidation[Any] #We don't enforce checks on JSONB schema on retrieve... only insert

class ProductUpdate(ProductBase):
    pass
