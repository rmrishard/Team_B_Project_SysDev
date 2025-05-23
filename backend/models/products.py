from typing import TypedDict
from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy.dialects.postgresql import JSONB

class ProductDetail(TypedDict, total=False):
    model_config = ConfigDict(extra='ignore')
    volume: str | None
    type: str | None
    certification: str | None
    arabic_text: str | None

class Product(SQLModel, table=True):
    model_config = ConfigDict(extra='ignore')
    id: int = Field(alias='product_id', primary_key=True)
    name: str
    description: str
    price: float
    image: str
    origin: str
    details: ProductDetail | None  = Field(sa_type=JSONB, nullable=False)