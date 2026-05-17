from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.core.config import Config
from src.app.infra.database import create_db_engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    config = Config()
    app.state.engine = create_db_engine(config=config)
    app.state.config = config
    try:
        yield
    finally:
        app.state.engine.dispose()


app = FastAPI(lifespan=lifespan)
