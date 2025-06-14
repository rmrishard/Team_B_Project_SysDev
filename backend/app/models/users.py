import uuid
from typing import TypedDict, Optional, Any
from decimal import Decimal
import datetime

from pydantic import ConfigDict, SkipValidation, AliasChoices
from sqlalchemy.dialects.postgresql.psycopg import JSONB
from sqlmodel import Field, SQLModel

# if referring to other models within this model (example)
# if TYPE_CHECKING:
#    from .team_model import Team

class UserBase(SQLModel):
    model_config = ConfigDict(extra='ignore')
    username: str
    email_address: str
    password: str
    creation_date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    account_verified: Optional[bool] = Field(default=False)
    account_status_type_id_fk: int = Field(alias='account_status_type_id', schema_extra={'serialization_alias': 'account_status_type_id'})
    first_name: str
    last_name: str
    mobile_phone: Optional[str] = Field(default=None)
    work_phone: Optional[str] = Field(default=None)
    home_phone: Optional[str] = Field(default=None)
    pref_billing_address_id_fk: Optional[uuid.UUID] = Field(alias='pref_billing_address_id',schema_extra={'serialization_alias': 'pref_billing_address_id'})
    pref_mailing_address_id_fk: Optional[uuid.UUID] = Field(alias='pref_mailing_address_id',schema_extra={'serialization_alias': 'pref_mailing_address_id'})
    contact_method_type_id_fk: Optional[int] = Field(alias='contact_method_type_id', schema_extra={'serialization_alias': 'contact_method_type_id'})
    user_role_type_id_fk: int = Field(alias='user_role_type_id', schema_extra={'serialization_alias': 'user_role_type_id'})

#When table=True validation is not done, thus it must be done manually
class User(UserBase, table=True):
    user_id_pk: uuid.UUID = Field(alias='id', primary_key=True, default_factory=uuid.uuid4, index=True,schema_extra={'serialization_alias': 'id'})

    # REQUIRED: This allows for helper functions to retrieve the appropriate id field
    @classmethod
    def getIdField(cls):
        return cls.user_id_pk

    # REQUIRED: This allows for helper functions to retrieve the appropriate human-name for the entity
    @classmethod
    def getName(cls):
        return "User"

class UserCreate(UserBase):
    account_status_type_id_fk: int = Field( schema_extra={'serialization_alias': 'account_status_type_id','validation_alias':AliasChoices('account_status_type_id')})
    pref_billing_address_id_fk: Optional[uuid.UUID] = Field( default=None, schema_extra={'serialization_alias': 'pref_billing_address_id','validation_alias':AliasChoices('pref_billing_address_id')})
    pref_mailing_address_id_fk: Optional[uuid.UUID] = Field( default=None, schema_extra={'serialization_alias': 'pref_mailing_address_id','validation_alias':AliasChoices('pref_mailing_address_id')})
    contact_method_type_id_fk: Optional[int] = Field( default=None, schema_extra={'serialization_alias': 'contact_method_type_id','validation_alias':AliasChoices('contact_method_type_id')})
    user_role_type_id_fk: int = Field( schema_extra={'serialization_alias': 'user_role_type_id','validation_alias':AliasChoices('user_role_type_id')})

    pass

class UserPublic(UserBase):
    user_id_pk: uuid.UUID = Field(alias='id',default_factory=uuid.uuid4, index=True,schema_extra={'serialization_alias': 'id'})

# Use this model when retrieving for public consumption
class UserPublicRetrieve(UserPublic):
    model_config = ConfigDict(extra='ignore')

#Use this model for updating a model in the database
class UserUpdate(UserBase):
    model_config = ConfigDict(extra='forbid')
    user_id_pk: None = Field(default=None, alias='id',schema_extra={'serialization_alias': 'id'}) # DON'T ALLOW PATCHES TO UPDATE PRIMARY KEY!!!
    username: Optional[str] = None
    email_address: Optional[str] = None
    password: Optional[str] = None
    creation_date: None = Field(default=None)   #Do not allow changing of creation date (init-only)
    account_verified: Optional[bool] = None
    account_status_type_id_fk: Optional[int] = Field(default=None, alias='account_status_type_id', schema_extra={'serialization_alias': 'account_status_type_id'})
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mobile_phone: Optional[str] = Field(default=None)
    work_phone: Optional[str] = Field(default=None)
    home_phone: Optional[str] = Field(default=None)
    pref_billing_address_id_fk: Optional[uuid.UUID] = Field(default=None, alias='pref_billing_address_id',schema_extra={'serialization_alias': 'pref_billing_address_id'})
    pref_mailing_address_id_fk: Optional[uuid.UUID] = Field(default=None, alias='pref_mailing_address_id',schema_extra={'serialization_alias': 'pref_mailing_address_id'})
    contact_method_type_id_fk: Optional[int] = Field(default=None, alias='contact_method_type_id', schema_extra={'serialization_alias': 'contact_method_type_id'})
    user_role_type_id_fk: Optional[int] = Field(default=None, alias='user_role_type_id', schema_extra={'serialization_alias': 'user_role_type_id'})

