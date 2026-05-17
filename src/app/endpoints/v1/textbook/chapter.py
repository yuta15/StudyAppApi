from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.app.core.exceptions import (
    DataNotFoundError,
    DatabaseError,
    DomainError,
    InvalidDataError,
    NetworkError,
    NotFoundError,
    UnauthorizedError,
)
from src.app.endpoints.deps import (
    get_add_chapter_dependencies,
    get_current_principal_id,
    get_modify_chapter_dependencies,
    get_modify_textbook_dependencies,
    get_session,
)
from src.app.model.textbook import TitleString
from src.app.schemas.api.textbook import (
    AddChapterInput,
    AddChapterOutput,
    ModifyChapterInput,
    ReorderChaptersInput,
)
from src.app.usecase.textbook import (
    AddChapterUsecase,
    ModifyChapterUsecase,
    RemoveChapterUsecase,
    ReorderChaptersUsecase,
)
from src.app.usecase.textbook.dependencies import (
    AddChapterDependencies,
    ModifyChapterDependencies,
    ModifyTextbookDependencies,
)
from src.app.usecase.textbook.dto import (
    AddChapterDTO,
    ModifyChapterDTO,
    RemoveChapterDTO,
    ReorderChaptersDTO,
)


chapter_router = APIRouter(prefix="/textbook/{textbook_id}/chapter", tags=["textbook-chapter"])


@chapter_router.post("/create", status_code=status.HTTP_201_CREATED)
def add_chapter(
    textbook_id: UUID,
    input: AddChapterInput,
    principal_id: UUID = Depends(get_current_principal_id),
    session: Session = Depends(get_session),
    dependencies: AddChapterDependencies = Depends(get_add_chapter_dependencies),
) -> AddChapterOutput:
    try:
        dto = AddChapterDTO(
            principal_id=principal_id,
            textbook_id=textbook_id,
            chapter_title=TitleString(value=input.chapter_title),
        )
        usecase = AddChapterUsecase(session=session, dependencies=dependencies)
        chapter_id = usecase.exec(add_chapter_dto=dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized.") from e
    except DataNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Textbook not found.") from e
    except InvalidDataError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid chapter data.") from e
    except NetworkError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable.") from e
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error.") from e

    return AddChapterOutput(chapter_id=chapter_id)


@chapter_router.post("/reorder", status_code=status.HTTP_204_NO_CONTENT)
def reorder_chapters(
    textbook_id: UUID,
    input: ReorderChaptersInput,
    principal_id: UUID = Depends(get_current_principal_id),
    session: Session = Depends(get_session),
    dependencies: ModifyTextbookDependencies = Depends(get_modify_textbook_dependencies),
) -> None:
    try:
        dto = ReorderChaptersDTO(
            principal_id=principal_id,
            textbook_id=textbook_id,
            chapter_ids=input.chapter_ids,
        )
        usecase = ReorderChaptersUsecase(session=session, dependencies=dependencies)
        usecase.exec(reorder_chapters_dto=dto)
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized.") from e
    except DataNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Textbook not found.") from e
    except InvalidDataError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid chapter data.") from e
    except NetworkError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable.") from e
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error.") from e


@chapter_router.post("/{chapter_id}", status_code=status.HTTP_204_NO_CONTENT)
def modify_chapter(
    textbook_id: UUID,
    chapter_id: UUID,
    input: ModifyChapterInput,
    principal_id: UUID = Depends(get_current_principal_id),
    session: Session = Depends(get_session),
    dependencies: ModifyChapterDependencies = Depends(get_modify_chapter_dependencies),
) -> None:
    try:
        dto = ModifyChapterDTO(
            principal_id=principal_id,
            textbook_id=textbook_id,
            chapter_id=chapter_id,
            title=TitleString(value=input.title) if input.title is not None else None,
            content=input.content,
        )
        usecase = ModifyChapterUsecase(session=session, dependencies=dependencies)
        usecase.exec(modify_chapter_dto=dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized.") from e
    except (DataNotFoundError, NotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found.") from e
    except InvalidDataError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid chapter data.") from e
    except NetworkError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable.") from e
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error.") from e


@chapter_router.delete("/{chapter_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_chapter(
    textbook_id: UUID,
    chapter_id: UUID,
    principal_id: UUID = Depends(get_current_principal_id),
    session: Session = Depends(get_session),
    dependencies: ModifyTextbookDependencies = Depends(get_modify_textbook_dependencies),
) -> None:
    try:
        dto = RemoveChapterDTO(
            principal_id=principal_id,
            textbook_id=textbook_id,
            chapter_id=chapter_id,
        )
        usecase = RemoveChapterUsecase(session=session, dependencies=dependencies)
        usecase.exec(remove_chapter_dto=dto)
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized.") from e
    except DataNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Textbook not found.") from e
    except InvalidDataError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid chapter data.") from e
    except NetworkError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable.") from e
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error.") from e
