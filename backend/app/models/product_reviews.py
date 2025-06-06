import datetime
import uuid

from typing import Optional
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel

class ProductReviewBase(SQLModel):
    __tablename__ = "product_review"
    model_config = ConfigDict(extra='ignore')
    product_id_fk: uuid.UUID = Field(alias='product_id', default_factory=uuid.uuid4,schema_extra={'serialization_alias': 'product_id'})
    user_id_fk: uuid.UUID = Field(alias='user_id', default_factory=uuid.uuid4, schema_extra={'serialization_alias': 'user_id'})
    rating: int
    title: Optional[str]
    content: Optional[str]
    verified_buyer: bool = Field(default=False)
    creation_time: datetime.datetime = Field(default_factory=datetime.datetime.now)

# When table=True validation is not done, thus it must be done manually
class ProductReview(ProductReviewBase, table=True):
    product_review_id_pk: uuid.UUID = Field(alias='id', primary_key=True, default_factory=uuid.uuid4, index=True, schema_extra={'serialization_alias': 'id'})

    # This allows for helper functions to retrieve the appropriate id field
    @classmethod
    def getIdField(cls):
        return cls.product_review_id_pk

class ProductReviewCreate(ProductReviewBase):
    pass

class ProductReviewPublic(ProductReviewBase):
    product_review_id_pk: uuid.UUID = Field(alias='id', primary_key=True, default_factory=uuid.uuid4, index=True, schema_extra={'serialization_alias': 'id'})

class ProductReviewUpdate(ProductReviewBase):
    pass





