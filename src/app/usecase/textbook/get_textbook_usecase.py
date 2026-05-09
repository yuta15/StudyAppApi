from sqlmodel import Session

from src.app.usecase.textbook.dto import TextbookDTO
from src.app.usecase.textbook.dependencies import GetTextbookDependencies
from src.app.service.domain_read_service.textbook import ReadTextbookDetailsModel, TextbookReadService
from src.app.service.authorization_service.textbook import TextbookAuthService
from src.app.service.authorization_service.account import AccountAuthService


class GetTextbookUsecase:
    def __init__(self, session: Session, dependencies: GetTextbookDependencies):
        self._session = session
        self._auth = TextbookAuthService(
            account_auth_service=AccountAuthService(repository=dependencies.account_auth_read),
            repository=dependencies.textbook_auth_read,
        )
        self._read = TextbookReadService(
            account_read=dependencies.account_read, textbook_read=dependencies.textbook_read
        )

    def exec(self, textbook_dto: TextbookDTO) -> ReadTextbookDetailsModel:
        with self._session.begin():
            self._auth.auth_read(principal_id=textbook_dto.principal_id, textbook_id=textbook_dto.textbook_id)
            return self._read.get_textbook_details(textbook_id=textbook_dto.textbook_id)
