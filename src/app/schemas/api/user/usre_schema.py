from uuid import UUID

from pydantic import BaseModel, EmailStr, SecretStr
from pydantic import EmailStr


class CreateUserInput(BaseModel):
    display_name:str
    username:str
    email:EmailStr
    password:SecretStr


class CreateUserOutput(BaseModel):
    id:UUID
    display_name:str