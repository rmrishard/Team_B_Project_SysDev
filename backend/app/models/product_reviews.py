import datetime
import uuid

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class ProductReviewBase(SQLModel):
    __tablename__ = "product_review"
    model_config = ConfigDict(extra='ignore')
    product_review_id_pk: uuid.UUID = Field(alias='id', primary_key=True, default_factory=uuid.uuid4, index=True)
    product_id_fk: uuid.UUID = Field(alias='product_id', default_factory=uuid.uuid4)
    user_id_fk: uuid.UUID = Field(alias='user_id', default_factory=uuid.uuid4)
    rating: int
    title: str
    content: str
    verified_buyer: bool
    creation_time: datetime.datetime

class ProductReviewCreate(ProductReviewBase):
    pass

#When table=True validation is not done, thus it must be done manually
class ProductReview(ProductReviewBase, table=True):
    pass