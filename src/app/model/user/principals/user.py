from uuid import uuid4
from dataclasses import dataclass
from typing import Self

from src.app.model.base.principal import Principal
from src.app.model.user.metadata.user_metadata import UserMetadata


@dataclass
class User(Principal):
    usenrame:str
    email:str
    hashed_password:str
    metadata:UserMetadata

    @classmethod
    def new(cls, display_name:str, username:str, email:str, hashed_password:str) -> Self:
        return User(
            id=uuid4(),
            display_name=display_name,
            username=username,
            email=email,
            hashed_password=hashed_password,
            metadata=UserMetadata.new()
        )

    def delete(self) -> None:
        deleted_value = "XXXXXXXXXXXX"
        self.usenrame = deleted_value
        self.email = deleted_value
        self.hashed_password = deleted_value
        self.metadata.delete()

    def set_new_password(self, new_hashed_password:str) -> None:
        self.hashed_password = new_hashed_password
        self.metadata.update()

    def set_new_email(self, new_email:str) -> None:
        self.email = new_email
        self.metadata.update()