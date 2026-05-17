from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from src.app.core.config import Config


def create_db_engine(config: Config) -> Engine:
    return create_engine(config.DB_URL)
