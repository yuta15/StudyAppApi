from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from firebase_admin import initialize_app

from src.app.core.config import Config
from src.app.infra.database import create_db_engine
from src.app.endpoints.v1 import v1_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    config = Config()
    app.state.engine = create_db_engine(config=config)
    app.state.config = config
    app.state.firebase_app = initialize_app(options={"projectId": config.FIREBASE_PROJECT_ID})
    try:
        yield
    finally:
        app.state.engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(v1_router)
