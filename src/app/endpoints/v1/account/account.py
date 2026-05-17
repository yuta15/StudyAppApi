from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.app.core.exceptions import DataNotFoundError, DatabaseError, InvalidDataError, NetworkError, UnauthorizedError
from src.app.endpoints.deps import (
    get_create_account_repositories,
    get_current_principal_id,
    get_delete_account_repositories,
    get_get_account_repositories,
    get_modify_account_repositories,
    get_session,
)
from src.app.model.account import AccountNameStrings, EmailStrings
from src.app.schemas.api.account import (
    AccountMetadataOutput,
    AccountOutput,
    AccountProfileOutput,
    AccountSettingsOutput,
    CreateAccountInput,
    CreateAccountOutput,
    ModifyAccountInput,
)
from src.app.usecase.account import (
    CreateAccountUsecase,
    DeleteAccountUsecase,
    GetAccountUsecase,
    ModifyAccountSettingsUsecase,
)
from src.app.usecase.account.dto import (
    AccountOutputDTO,
    CreateAccountDTO,
    ModifyAccountDTO,
    ModifyBasicSettings,
    ModifyProfile,
)
from src.app.usecase.account.repository import (
    CreateAccountRepositories,
    DeleteAccountRepositories,
    GetAccountRepositories,
    ModifyAccountRepositories,
)


account_router = APIRouter(prefix="/account", tags=["account"])


@account_router.post("/create", status_code=status.HTTP_201_CREATED)
def create_account(
    input: CreateAccountInput,
    session: Session = Depends(get_session),
    repositories: CreateAccountRepositories = Depends(get_create_account_repositories),
) -> CreateAccountOutput:
    try:
        dto = CreateAccountDTO(
            account_name=AccountNameStrings(value=input.account_name),
            display_name=input.display_name,
            email=EmailStrings(value=str(input.email)),
            subject=input.subject,
            provider=input.provider,
        )
        usecase = CreateAccountUsecase(session=session, repositories=repositories)
        principal_id = usecase.exec(create_account_dto=dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except InvalidDataError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid account data.") from e
    except NetworkError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable.") from e
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error.") from e

    return CreateAccountOutput(id=principal_id)


@account_router.get("/me")
def get_account(
    principal_id: UUID = Depends(get_current_principal_id),
    session: Session = Depends(get_session),
    repositories: GetAccountRepositories = Depends(get_get_account_repositories),
) -> AccountOutput:
    try:
        usecase = GetAccountUsecase(session=session, repositories=repositories)
        output = usecase.exec(principal_id=principal_id)
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized.") from e
    except DataNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found.") from e
    except NetworkError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable.") from e
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error.") from e

    return _to_account_output(output=output)


@account_router.post("/me")
def modify_account(
    input: ModifyAccountInput,
    principal_id: UUID = Depends(get_current_principal_id),
    session: Session = Depends(get_session),
    repositories: ModifyAccountRepositories = Depends(get_modify_account_repositories),
) -> AccountOutput:
    try:
        dto = ModifyAccountDTO(
            principal_id=principal_id,
            profile=ModifyProfile(
                display_name=input.profile.display_name,
                email=EmailStrings(value=str(input.profile.email)) if input.profile.email is not None else None,
                country=input.profile.country,
            ),
            basic_settings=ModifyBasicSettings(is_public=input.basic_settings.is_public),
        )
        usecase = ModifyAccountSettingsUsecase(session=session, repositories=repositories)
        output = usecase.exec(modify_account_dto=dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized.") from e
    except DataNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found.") from e
    except InvalidDataError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid account data.") from e
    except NetworkError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable.") from e
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error.") from e

    return _to_account_output(output=output)


@account_router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    principal_id: UUID = Depends(get_current_principal_id),
    session: Session = Depends(get_session),
    repositories: DeleteAccountRepositories = Depends(get_delete_account_repositories),
) -> None:
    try:
        usecase = DeleteAccountUsecase(session=session, repositories=repositories)
        usecase.exec(principal_id=principal_id)
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized.") from e
    except DataNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found.") from e
    except InvalidDataError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid account data.") from e
    except NetworkError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable.") from e
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error.") from e


def _to_account_output(output: AccountOutputDTO) -> AccountOutput:
    return AccountOutput(
        principal_id=output.principal_id,
        account_name=output.account_name.value,
        status=output.status,
        metadata=AccountMetadataOutput(
            created_at=output.metadata.created_at,
            last_update=output.metadata.last_update,
        ),
        profile=AccountProfileOutput(
            display_name=output.profile.display_name,
            email=output.profile.email.value,
            country=output.profile.country,
        ),
        settings=AccountSettingsOutput(is_public=output.settings.is_public),
    )
