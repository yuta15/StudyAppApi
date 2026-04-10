from uuid import UUID
from dataclasses import dataclass

from src.app.model.account.entities.value_object import AccountNameStrings, EmailStrings


@dataclass
class CreateAccountDTO:
    account_name:AccountNameStrings
    display_name:str
    email:EmailStrings
    plain_password:str


@dataclass
class LoginDTO:
    principal_id:UUID
    plain_password:str