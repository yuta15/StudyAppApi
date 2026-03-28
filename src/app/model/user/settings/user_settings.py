from uuid import UUID
from dataclasses import dataclass

from src.app.model.base.enum import Country


@dataclass
class UserBasicSettings:
    username:str
    email:str
    country:Country
    hashed_password:str
    is_public:bool


@dataclass
class UserSettings:
    user_id:UUID
    basic:UserBasicSettings


