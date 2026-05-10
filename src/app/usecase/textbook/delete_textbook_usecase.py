from src.app.model.textbook.service import DeleteTextbookData, DeleteTextbookDomainService
from src.app.usecase.textbook.dependencies import DeleteTextbookDependencies
from src.app.usecase.textbook.dto import TextbookDTO
from src.app.usecase.textbook.textbook_usecase_base import TextbookUsecaseBase


class DeleteTextbookUsecase(TextbookUsecaseBase[DeleteTextbookDependencies]):
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
