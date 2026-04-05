from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Self
from uuid import UUID, uuid4


class AccountSubjcects(Enum):
    ACCOUNT_PROFILE = "ACCOUNT_PROFILE"
    ACCOUNT_BASIC_SETTINGS = "ACCOUNT_BASIC_SETTINGS"
    ACCOUNT_AUTH_SETTINGS = "ACCOUNT_AUTH_SETTINGS"


class Location(Enum):
    JP = "JP"
    US = "US"


@dataclass
class AccountSubject(ABC):
    """権限を持つ対象"""
    principal_id:UUID
    subject_id:UUID

    @abstractmethod
    @classmethod
    def new(cls, principal_id:UUID, **kwargs) -> Self:...

    @abstractmethod
    def delete(self) -> None:...


@dataclass
class AccountProfile(AccountSubject):
    name:str
    email:str
    country:str | None

    @classmethod
    def new(cls, principal_id:UUID, name:str, email:str, **kwargs) -> Self:
        return AccountProfile(
            principal_id=principal_id,
            subject_id=uuid4(),
            name=name,
            email=email,
            country=None
        )

    def delete(self):
        MASK_VALUE = "XXXXXXXXXX"
        self.name = MASK_VALUE
        self.email = MASK_VALUE

    def set_email(self, email:str) -> None:
        self.email = email
    
    def set_country(self, country:str) -> None:
        self.country = country


class AccountProfileAuthorizations(Enum):
    MODIFY = "MODIFY"


@dataclass
class AccountBasicSettings(AccountSubject):
    is_public:bool = False

    @classmethod
    def new(cls, principal_id:UUID, **kwargs) -> Self:
        return AccountBasicSettings(
            principal_id=principal_id,
            subject_id=uuid4(),
        )

    def delete(self):
        self.is_public = False

    def set_is_public(self, is_public:bool) -> None:
        self.is_public = is_public


class AccountBasicSettingsAuthorizations(Enum):
    MODIFY = "MODIFY"


@dataclass
class AccountAuthSettins(AccountSubject):
    hashed_password:str

    @classmethod
    def new(cls, principal_id:UUID, hashed_password:str, **kwargs) -> Self:
        return AccountAuthSettins(
            principal_id=principal_id,
            subject_id=uuid4(),
            hashed_password=hashed_password
        )

    def delete(self):
        MASK_VALUE = "XXXXXXXXXX"
        self.hashed_password = MASK_VALUE

    def set_hashed_password(self, hashed_password:str) -> None:
        self.hashed_password = hashed_password


class AccountAuthSettinsAuthorizations(Enum):
    MODIFY = "MODIFY"