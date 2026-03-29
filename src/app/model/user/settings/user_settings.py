from uuid import UUID
from typing import Self
from dataclasses import dataclass

from src.app.model.base.enum import Country


@dataclass
class UserBasicSettings:
    is_public:bool=True
    country:Country|None=None

    def delete(self) -> None:
        self.country = None
        self.is_public = False


@dataclass
class UserSettings:
    user_id:UUID    
    basic:UserBasicSettings

    @classmethod
    def new(cls) -> Self:
        return UserSettings(
            basic=UserBasicSettings()
        )
    
    def delete(self) -> None:
        self.basic.delete()