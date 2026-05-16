from uuid import UUID

from sqlmodel import SQLModel, Field


class TableBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)


class IncludePrincipalTableBase(TableBase):
    principal_id: UUID = Field(nullable=False, unique=True)
