from sqlmodel import SQLModel, Field


class TableBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
