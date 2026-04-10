from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Self
from uuid import UUID, uuid4

from src.app.model.account.entities.validation import validate_value_type
from src.app.model.account.entities.value_object import EmailStrings


class AccountSubjects(Enum):
    ACCOUNT_PROFILE = "ACCOUNT_PROFILE"
    ACCOUNT_BASIC_SETTINGS = "ACCOUNT_BASIC_SETTINGS"
    ACCOUNT_AUTH_SETTINGS = "ACCOUNT_AUTH_SETTINGS"


class Country(Enum):
    NOT_SET = "NOT_SET"
    JP = "JP"
    US = "US"


@dataclass
class AccountSubject(ABC):
    """権限を持つ対象"""
    principal_id:UUID
    subject_id:UUID

    @classmethod
    @abstractmethod
    def new(cls, principal_id:UUID, **kwargs) -> Self:...

    @abstractmethod
    def delete(self) -> None:...


@dataclass
class AccountProfile(AccountSubject):
    display_name:str
    email:EmailStrings
    country:Country = Country.NOT_SET

    @classmethod
    def new(cls, principal_id:UUID, display_name:str, email:EmailStrings, **kwargs) -> Self:
        validate_value_type(value=principal_id, valid_type=UUID)
        validate_value_type(value=display_name, valid_type=str)
        validate_value_type(value=email, valid_type=EmailStrings)
        return AccountProfile(
            principal_id=principal_id,
            subject_id=uuid4(),
            display_name=display_name,
            email=email,
        )

    def delete(self):
        MASK_VALUE = "XXXXXXXXXX"
        self.display_name = MASK_VALUE
        self.email = f"{MASK_VALUE}@{MASK_VALUE}"

    def set_display_name(self, display_name:str) -> None:
        validate_value_type(value=display_name, valid_type=str)
        self.display_name = display_name

    def set_email(self, email:EmailStrings) -> None:
        validate_value_type(value=email, valid_type=EmailStrings)
        self.email = email
    
    def set_country(self, country:Country) -> None:
        validate_value_type(value=country, valid_type=Country)
        self.country = country


@dataclass
class AccountBasicSettings(AccountSubject):
    is_public:bool = True

    @classmethod
    def new(cls, principal_id:UUID, **kwargs) -> Self:
        validate_value_type(value=principal_id, valid_type=UUID)
        return AccountBasicSettings(
            principal_id=principal_id,
            subject_id=uuid4(),
        )

    def delete(self):
        self.is_public = False

    def set_is_public(self, is_public:bool) -> None:
        validate_value_type(value=is_public, valid_type=bool)
        self.is_public = is_public



@dataclass
class AccountAuthSettings(AccountSubject):
    hashed_password:str

    @classmethod
    def new(cls, principal_id:UUID, hashed_password:str, **kwargs) -> Self:
        validate_value_type(value=principal_id, valid_type=UUID)
        validate_value_type(value=hashed_password, valid_type=str)
        return cls(
            principal_id=principal_id,
            subject_id=uuid4(),
            hashed_password=hashed_password
        )

    def delete(self):
        MASK_VALUE = "XXXXXXXXXX"
        self.hashed_password = MASK_VALUE

    def set_hashed_password(self, hashed_password:str) -> None:
        validate_value_type(value=hashed_password, valid_type=str)
        self.hashed_password = hashed_password