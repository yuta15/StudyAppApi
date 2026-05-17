from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.app.core.exceptions import (
    DataNotFoundError,
    DatabaseError,
    InvalidDataError,
    NetworkError,
    UnauthorizedError,
)
from src.app.endpoints.deps import (
    get_create_textbook_dependencies,
    get_current_principal_id,
    get_delete_textbook_dependencies,
    get_get_textbook_dependencies,
    get_modify_textbook_dependencies,
    get_optional_principal_id,
    get_session,
)
from src.app.model.textbook import TitleString
from src.app.schemas.api.textbook import (
    CreateTextbookInput,
    CreateTextbookOutput,
    MinimalAccountOutput,
    MinimalChapterOutput,
    ModifyTextbookInput,
    ModifyTextbookOutput,
    TextbookMetadataOutput,
    TextbookOutput,
)
from src.app.service.domain_read_service.textbook import ReadTextbookDetailsModel
from src.app.usecase.textbook import (
    CreateTextbookUsecase,
    DeleteTextbookUsecase,
    GetTextbookUsecase,
    ModifyTextbookUsecase,
)
from src.app.usecase.textbook.dependencies import (
    CreateTextbookDependencies,
    DeleteTextbookDependencies,
    GetTextbookDependencies,
    ModifyTextbookDependencies,
)
from src.app.usecase.textbook.dto import (
    CreateTextbookDTO,
    ModifyTextbookDTO,
    OutputTextbookModified,
    TextbookDTO,
)


textbook_router = APIRouter(prefix="/textbook", tags=["textbook"])


@textbook_router.post("/create", status_code=status.HTTP_201_CREATED)
def create_textbook(
    input: CreateTextbookInput,
    principal_id: UUID = Depends(get_current_principal_id),
    session: Session = Depends(get_session),
    dependencies: CreateTextbookDependencies = Depends(get_create_textbook_dependencies),
) -> CreateTextbookOutput:
    try:
        dto = CreateTextbookDTO(
            principal_id=principal_id,
            title=TitleString(value=input.title),
        )
        usecase = CreateTextbookUsecase(session=session, dependencies=dependencies)
        textbook_id = usecase.exec(create_textbook_dto=dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized.") from e
    except InvalidDataError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid textbook data.") from e
    except NetworkError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable.") from e
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error.") from e

    return CreateTextbookOutput(textbook_id=textbook_id)


@textbook_router.get("/{textbook_id}")
def get_textbook(
    textbook_id: UUID,
    principal_id: UUID | None = Depends(get_optional_principal_id),
    session: Session = Depends(get_session),
    dependencies: GetTextbookDependencies = Depends(get_get_textbook_dependencies),
) -> TextbookOutput:
    try:
        dto = TextbookDTO(principal_id=principal_id, textbook_id=textbook_id)
        usecase = GetTextbookUsecase(session=session, dependencies=dependencies)
        output = usecase.exec(textbook_dto=dto)
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized.") from e
    except DataNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Textbook not found.") from e
    except NetworkError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable.") from e
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error.") from e

    return _to_textbook_output(output=output)


@textbook_router.post("/{textbook_id}")
def modify_textbook(
    textbook_id: UUID,
    input: ModifyTextbookInput,
    principal_id: UUID = Depends(get_current_principal_id),
    session: Session = Depends(get_session),
    dependencies: ModifyTextbookDependencies = Depends(get_modify_textbook_dependencies),
) -> ModifyTextbookOutput:
    try:
        dto = ModifyTextbookDTO(
            principal_id=principal_id,
            textbook_id=textbook_id,
            title=TitleString(value=input.title) if input.title is not None else None,
            status=input.status,
        )
        usecase = ModifyTextbookUsecase(session=session, dependencies=dependencies)
        output = usecase.exec(modify_textbook_dto=dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized.") from e
    except DataNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Textbook not found.") from e
    except InvalidDataError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid textbook data.") from e
    except NetworkError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable.") from e
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error.") from e

    return _to_modify_textbook_output(output=output)


@textbook_router.delete("/{textbook_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_textbook(
    textbook_id: UUID,
    principal_id: UUID = Depends(get_current_principal_id),
    session: Session = Depends(get_session),
    dependencies: DeleteTextbookDependencies = Depends(get_delete_textbook_dependencies),
) -> None:
    try:
        dto = TextbookDTO(principal_id=principal_id, textbook_id=textbook_id)
        usecase = DeleteTextbookUsecase(session=session, dependencies=dependencies)
        usecase.exec(textbook_dto=dto)
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized.") from e
    except DataNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Textbook not found.") from e
    except InvalidDataError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid textbook data.") from e
    except NetworkError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable.") from e
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error.") from e


def _to_textbook_output(output: ReadTextbookDetailsModel) -> TextbookOutput:
    authors = []
    for author in output.authors:
        authors.append(
            MinimalAccountOutput(
                principal_id=author.principal_id,
                account_name=author.account_name.value,
            )
        )

    chapters = []
    for chapter in output.chapters:
        chapters.append(
            MinimalChapterOutput(
                chapter_id=chapter.chapter_id,
                title=chapter.title.value,
            )
        )

    return TextbookOutput(
        textbook_id=output.textbook_id,
        title=output.title.value,
        status=output.status,
        authors=authors,
        chapters=chapters,
        metadata=TextbookMetadataOutput(
            created_at=output.metadata.created_at,
            updated_at=output.metadata.updated_at,
        ),
    )


def _to_modify_textbook_output(output: OutputTextbookModified) -> ModifyTextbookOutput:
    return ModifyTextbookOutput(
        textbook_id=output.textbook_id,
        title=output.title.value,
        status=output.status,
        metadata=TextbookMetadataOutput(
            created_at=output.metadata.created_at,
            updated_at=output.metadata.updated_at,
        ),
    )
