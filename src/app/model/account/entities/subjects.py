from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Self
from uuid import UUID, uuid4


class AccountSubjcects(Enum):
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
    email:str
    country:Country = Country.NOT_SET

    @classmethod
    def new(cls, principal_id:UUID, display_name:str, email:str, **kwargs) -> Self:
        return AccountProfile(
            principal_id=principal_id,
            subject_id=uuid4(),
            display_name=display_name,
            email=email,
        )

    def delete(self):
        MASK_VALUE = "XXXXXXXXXX"
        self.display_name = MASK_VALUE
        self.email = MASK_VALUE

    def set_display_name(self, display_name:str) -> None:
        if not isinstance(display_name, str):
            raise ValueError("display_nameが文字列じゃないよ")
        self.display_name = display_name

    def set_email(self, email:str) -> None:
        if not isinstance(email, str):
            raise ValueError("emailが文字列じゃないよ")
        self.email = email
    
    def set_country(self, country:Country) -> None:
        if not isinstance(country, Country):
            raise ValueError("国名じゃないよ")
        self.country = country


@dataclass
class AccountBasicSettings(AccountSubject):
    is_public:bool = True

    @classmethod
    def new(cls, principal_id:UUID, **kwargs) -> Self:
        return AccountBasicSettings(
            principal_id=principal_id,
            subject_id=uuid4(),
        )

    def delete(self):
        self.is_public = False

    def set_is_public(self, is_public:bool) -> None:
        if not isinstance(is_public, bool):
            raise ValueError("boolしかとらないよ")
        self.is_public = is_public



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
        if not isinstance(hashed_password, str):
            raise ValueError("passwordはStrを入れてね")
        self.hashed_password = hashed_password