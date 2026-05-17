from src.app.endpoints.deps.account import (
    get_create_account_repositories,
    get_delete_account_repositories,
    get_get_account_repositories,
    get_modify_account_repositories,
)
from src.app.endpoints.deps.auth import get_current_principal_id, get_optional_principal_id
from src.app.endpoints.deps.db import get_session
from src.app.endpoints.deps.textbook import (
    get_add_chapter_dependencies,
    get_create_textbook_dependencies,
    get_delete_textbook_dependencies,
    get_get_textbook_dependencies,
    get_modify_chapter_dependencies,
    get_modify_textbook_dependencies,
    get_modify_textbook_settings_dependencies,
    get_get_chapter_dependencies,
)

__all__ = [
    "get_add_chapter_dependencies",
    "get_create_account_repositories",
    "get_current_principal_id",
    "get_create_textbook_dependencies",
    "get_delete_account_repositories",
    "get_delete_textbook_dependencies",
    "get_get_account_repositories",
    "get_get_textbook_dependencies",
    "get_modify_chapter_dependencies",
    "get_modify_account_repositories",
    "get_modify_textbook_dependencies",
    "get_modify_textbook_settings_dependencies",
    "get_optional_principal_id",
    "get_get_chapter_dependencies",
    "get_session",
]
