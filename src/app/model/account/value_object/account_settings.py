from uuid import UUID
from abc import ABC, abstractmethod
from typing import Self
from dataclasses import dataclass

from src.app.model.base.enum import Country


@dataclass
class AccountSettings(ABC):
    account_id:UUID
    @abstractmethod
    def delete(self) -> None:...


@dataclass
class Profile(AccountSettings):
    email:str
    country:Country|None=None

    @classmethod
    def new(cls, account_id:UUID, email:str) -> Self:
        return Profile(account_id=account_id, email=email)
    
    def delete(self):
        self.email = None
        self.country = None

    def update_country(self, country:Country) -> None:
        if isinstance(country, Country):
            self.country = country

    def update_email(self, email:str) -> None:
        if isinstance(email, str):
            self.email = email


@dataclass
class BasicSettings(AccountSettings):
    is_public:bool=True

    @classmethod
    def new(cls, account_id:UUID) -> Self:
        return BasicSettings(account_id=account_id)

    def delete(self) -> None:
        self.is_public = False

    def update_public_settings(self, is_public:bool):
        self.is_public = is_public


@dataclass
class AuthSettings(AccountSettings):
    hashed_password:str

    @classmethod
    def new(cls, account_id:UUID, hashed_password:str) -> Self:
        return AuthSettings(account_id=account_id, hashed_password=hashed_password)

    def update_hashed_password(self, hashed_password:str) -> None:
        self.hashed_password = hashed_password

    def delete(self) -> None:
        self.hashed_password = None