from pydantic_settings import BaseSettings
from sqlalchemy import URL


class MigrationSettings(BaseSettings):
    DB_MIGRATION_USER: str
    DB_MIGRATION_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    @property
    def DB_URL(self) -> str:
        return URL.create(
            drivername="postgresql+psycopg",
            username=self.DB_MIGRATION_USER,
            password=self.DB_MIGRATION_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        ).render_as_string(hide_password=False)
