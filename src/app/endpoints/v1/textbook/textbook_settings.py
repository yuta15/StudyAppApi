from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.app.core.exceptions import DataNotFoundError, DatabaseError, InvalidDataError, NetworkError, UnauthorizedError
from src.app.endpoints.deps import (
    get_current_principal_id,
    get_modify_textbook_settings_dependencies,
    get_session,
)
from src.app.schemas.api.textbook import ModifyTextbookSettingsInput
from src.app.usecase.textbook import ModifyTextbookSettingsUsecase
from src.app.usecase.textbook.dependencies import ModifyTextbookSettingsDependencies
from src.app.usecase.textbook.dto import ModifyTextbookSettingsDTO


textbook_settings_router = APIRouter(prefix="/textbook/{textbook_id}/settings", tags=["textbook-settings"])


@textbook_settings_router.post("", status_code=status.HTTP_204_NO_CONTENT)
def modify_textbook_settings(
    textbook_id: UUID,
    input: ModifyTextbookSettingsInput,
    principal_id: UUID = Depends(get_current_principal_id),
    session: Session = Depends(get_session),
    dependencies: ModifyTextbookSettingsDependencies = Depends(get_modify_textbook_settings_dependencies),
) -> None:
    try:
        dto = ModifyTextbookSettingsDTO(
            principal_id=principal_id,
            textbook_id=textbook_id,
            is_public=input.is_public,
        )
        usecase = ModifyTextbookSettingsUsecase(session=session, dependencies=dependencies)
        usecase.exec(modify_textbook_settings_dto=dto)
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized.") from e
    except DataNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Textbook settings not found.") from e
    except InvalidDataError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid textbook settings data.") from e
    except NetworkError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable.") from e
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error.") from e
