import uuid
from typing import TypedDict, Optional

from pydantic import ConfigDict
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel

# if referring to other models within this model (example)
# if TYPE_CHECKING:
#    from .team_model import Team

class ProductDetail(TypedDict, total=False):
    volume: str | None # either string or null, or this syntax
    type: Optional[str]
    certification: str | None
    arabic_text: str | None

class ImageDetail(SQLModel):
    url: str
    label: str
    width: Optional[int] = Field(default=None, nullable=True)
    height: Optional[int] = Field(default=None, nullable=True)

class ProductBase(SQLModel):
    model_config = ConfigDict(extra='ignore')
    id: uuid.UUID = Field(alias='product_id', primary_key=True, default_factory=uuid.uuid4, index=True)
    name: str
    description: str
    price: float
    weight: Optional[float] = Field(default=None)
    dimensions: Optional[str] = Field(default=None)
    stock_quantity: int = Field(default=0)
    image: list[ImageDetail] | None = Field(sa_type=JSONB, nullable=False)
    origin: str
    details: ProductDetail | None  = Field(sa_type=JSONB, nullable=False)

class ProductCreate(ProductBase):
    pass

#When table=True validation is not done, thus it must be done manually
class Product(ProductBase, table=True):
    pass