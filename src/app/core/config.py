from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Config(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")
    DB_APP_USER: str
    DB_APP_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    @property
    def DB_URL(self) -> str:
        return URL.create(
            drivername="postgresql+psycopg",
            username=self.DB_APP_USER,
            password=self.DB_APP_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        ).render_as_string(hide_password=False)
