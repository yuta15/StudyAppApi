from fastapi import APIRouter

from src.app.endpoints.v1.account.account import account_router
from src.app.endpoints.v1.textbook.textbook import textbook_router
from src.app.endpoints.v1.textbook.textbook_settings import textbook_settings_router
from src.app.endpoints.v1.textbook.chapter import chapter_router


v1_router = APIRouter()

v1_router.include_router(account_router)
v1_router.include_router(textbook_router)
v1_router.include_router(textbook_settings_router)
v1_router.include_router(chapter_router)
