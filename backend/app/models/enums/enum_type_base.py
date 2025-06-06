from typing import Optional
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel

class EnumTypeBase(SQLModel):
    model_config = ConfigDict(extra='ignore')
    label: str
    description: Optional[str]
    category: Optional[str] = Field(index=True)
    active: bool = True
