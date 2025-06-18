import datetime
import uuid

from typing import Optional, Annotated, TYPE_CHECKING, TypedDict, List
from pydantic import ConfigDict, AliasChoices, BaseModel
from sqlmodel import Field

class Credential(BaseModel):
    model_config = ConfigDict(extra='forbid')
    username: Optional[str]
    guest_token: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)
    user_id: Optional[uuid.UUID] = Field(default=None)
    role: Optional[str|int] = None