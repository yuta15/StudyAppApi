from dataclasses import dataclass
from uuid import UUID

from src.app.model.account.entities.value_object import AccountNameStrings, EmailStrings
from src.app.model.account.entities.subjects import AllowedIdentityProvider, Country


@dataclass
class CreateAccountDTO:
    account_name:AccountNameStrings
    display_name:str
    email:EmailStrings
    subject:str
    provider:AllowedIdentityProvider


@dataclass
class ModifyProfile:
    display_name:str|None
    email:EmailStrings|None
    country:Country|None


@dataclass
class ModifyBasicSettings:
    is_public:bool|None


@dataclass
class ModifyAccountDTO:
    principal_id:UUID
    profile:ModifyProfile|None
    basic_settings:ModifyBasicSettings|None