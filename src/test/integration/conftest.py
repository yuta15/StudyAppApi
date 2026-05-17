import pytest
from sqlalchemy import create_engine
from sqlmodel import Session

from src.app.core.config import Config


@pytest.fixture(scope="session")
def integration_config() -> Config:
    return Config(_env_file=".env")


@pytest.fixture(scope="session")
def integration_engine(integration_config: Config):
    return create_engine(integration_config.DB_URL)


@pytest.fixture
def infra_session(integration_engine):
    with Session(integration_engine) as session:
        yield session
        session.rollback()
