from sqlmodel import Session

from src.app.service.domain_read_service.textbook import ReadTextbookDetailsModel, TextbookReadService
from src.app.usecase.textbook.dependencies import GetTextbookDependencies
from src.app.usecase.textbook.dto import TextbookDTO
from src.app.usecase.textbook.textbook_usecase_base import TextbookUsecaseBase


class GetTextbookUsecase(TextbookUsecaseBase[GetTextbookDependencies]):
    def __init__(self, session: Session, dependencies: GetTextbookDependencies):
        super().__init__(session=session, dependencies=dependencies)
        self._read = TextbookReadService(
            account_read=dependencies.account_read, textbook_read=dependencies.textbook_read
        )

    def exec(self, textbook_dto: TextbookDTO) -> ReadTextbookDetailsModel:
        with self._session.begin():
            self._textbook_auth.auth_read(principal_id=textbook_dto.principal_id, textbook_id=textbook_dto.textbook_id)
            return self._read.get_textbook_details(textbook_id=textbook_dto.textbook_id)
