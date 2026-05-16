from src.app.usecase.textbook.dependencies import ModifyTextbookSettingsDependencies
from src.app.usecase.textbook.dto import ModifyTextbookSettingsDTO
from src.app.model.textbook.service import ModifyTextbookSettingsDomainService
from src.app.usecase.textbook.textbook_usecase_base import TextbookUsecaseBase


class GetTextbookSettingsUsecase(TextbookUsecaseBase[ModifyTextbookSettingsDependencies]):
    def exec(self, modify_textbook_settings_dto: ModifyTextbookSettingsDTO) -> None:
        with self._session.begin():
            self._textbook_auth.auth_manage(
                principal_id=modify_textbook_settings_dto.principal_id,
                textbook_id=modify_textbook_settings_dto.textbook_id,
            )

            textbook_settings = self._dependencies.settings.get(textbook_id=modify_textbook_settings_dto.principal_id)
            metadata = self._dependencies.metadata.get(textbook_id=modify_textbook_settings_dto.textbook_id)
            is_changed = ModifyTextbookSettingsDomainService.update_settings(
                settings=textbook_settings, metadata=metadata, is_public=modify_textbook_settings_dto.is_public
            )

            if is_changed:
                self._dependencies.settings.save(textbook_settings=textbook_settings)
                self._dependencies.metadata.save(metadata=metadata)
