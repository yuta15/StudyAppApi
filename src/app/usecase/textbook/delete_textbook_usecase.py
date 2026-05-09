from sqlmodel import Session

from src.app.usecase.textbook.dto import TextbookDTO
from src.app.service.authorization_service.textbook import TextbookAuthService
from src.app.service.authorization_service.account import AccountAuthService

from src.app.usecase.textbook.dependencies import DeleteTextbookDependencies
from src.app.model.textbook.service import DeleteTextbookData, DeleteTextbookDomainService


class DeleteTextbookUsecase:
    def __init__(self, session: Session, dependencies: DeleteTextbookDependencies):
        self._session = session
        self._dependencies = dependencies
        self._textbook_auth = TextbookAuthService(
            account_auth_service=AccountAuthService(repository=dependencies.account_auth_read),
            repository=dependencies.textbook_auth_read,
        )

    def exec(self, textbook_dto: TextbookDTO) -> None:
        with self._session.begin():
            # 認可
            self._textbook_auth.auth_manage(
                principal_id=textbook_dto.principal_id, textbook_id=textbook_dto.textbook_id
            )
            # 現在の値の取得
            metadata = self._dependencies.metadata.get(textbook_id=textbook_dto.textbook_id)
            settings = self._dependencies.settings.get(textbook_id=textbook_dto.textbook_id)
            # 更新
            input = DeleteTextbookData(metadata=metadata, settings=settings)
            DeleteTextbookDomainService.exec(delete_textbook_data=input)
            # 保存
            self._dependencies.metadata.save(metadata=metadata)
            self._dependencies.settings.save(textbook_settings=settings)
