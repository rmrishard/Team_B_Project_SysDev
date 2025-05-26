import uuid
from typing import TYPE_CHECKING, TypedDict, Optional, List
from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy.dialects.postgresql import JSONB

# if referring to other models within this model (example)
# if TYPE_CHECKING:
#    from .team_model import Team

class ProductDetail(TypedDict, total=False):
    model_config = ConfigDict(extra='ignore')
    volume: str | None # either string or null, or this syntax
    type: Optional[str]
    certification: str | None
    arabic_text: str | None

class ImageDetail(TypedDict, total=False):
    model_config = ConfigDict(extra='ignore')
    url: Optional[str]
    label: Optional[str]
    width: Optional[int]
    height: Optional[int]

class Product(SQLModel, table=True):
    model_config = ConfigDict(extra='ignore')
    id: uuid.UUID = Field(alias='product_id', primary_key=True)
    name: str
    description: str
    price: float
    weight: float
    dimensions: str
    stock_quantity: int
    image: Optional[List[ImageDetail]] = Field(sa_type=JSONB, nullable=False)
    origin: str
    details: ProductDetail | None  = Field(sa_type=JSONB, nullable=False)