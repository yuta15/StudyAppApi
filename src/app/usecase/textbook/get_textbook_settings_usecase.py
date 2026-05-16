from src.app.usecase.textbook.dependencies import GetTextbookSettingsDependencies
from src.app.usecase.textbook.dto import GetTextbookSettingsOutputDTO, TextbookDTO, TextbookSettingsDTO
from src.app.usecase.textbook.textbook_usecase_base import TextbookUsecaseBase


class GetTextbookSettingsUsecase(TextbookUsecaseBase[GetTextbookSettingsDependencies]):
    def exec(self, textbook_dto: TextbookDTO) -> GetTextbookSettingsOutputDTO:
        with self._session.begin():
            self._textbook_auth.auth_manage(
                principal_id=textbook_dto.principal_id,
                textbook_id=textbook_dto.textbook_id,
            )

            settings = self._dependencies.settings.get(textbook_id=textbook_dto.textbook_id)

            return GetTextbookSettingsOutputDTO(
                textbook_id=textbook_dto.textbook_id, settings=TextbookSettingsDTO(is_public=settings.is_public)
            )
