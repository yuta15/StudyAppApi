from src.app.model.shared.validation import validate_value_type
from src.app.model.textbook import TextbookMetadata, TextbookSettings


class ModifyTextbookSettingsDomainService:
    """TextbookSettingsの変更ルールを管理する。"""

    @staticmethod
    def update_settings(
        settings: TextbookSettings,
        metadata: TextbookMetadata,
        is_public: bool | None = None,
    ) -> bool:
        """教材設定を変更し、実際に変更があった場合のみmetadataを更新する。"""
        if is_public is not None:
            validate_value_type(value=is_public, valid_type=bool)

        if is_public is None or is_public == settings.is_public:
            return False

        settings.set_is_public(is_public=is_public)
        metadata.update()
        return True
