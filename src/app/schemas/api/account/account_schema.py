from uuid import UUID

from pydantic import BaseModel, EmailStr, SecretStr


class CreateAccountInput(BaseModel):
    display_name:str
    email:EmailStr
    password:SecretStr


class CreateAccountOutput(BaseModel):
    id:UUID
    display_name:str


class BaseAccountInput(BaseModel):
    id:UUID