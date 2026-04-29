from uuid import UUID

from pydantic import BaseModel, EmailStr


class CreateAccountInput(BaseModel):
    display_name: str
    email: EmailStr


class CreateAccountOutput(BaseModel):
    id: UUID
    display_name: str


class BaseAccountInput(BaseModel):
    id: UUID
