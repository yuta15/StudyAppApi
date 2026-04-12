from src.app.model.account.entities.value_object import EmailStrings
from src.app.model.account.entities.metadata import AccountMetadata
from src.app.model.account.entities.subjects import (
    Country,
    AccountProfile,
    AccountBasicSettings,
)


class UpdateSubjectsDomainService:
    @staticmethod
    def update_profile(
            target_profile:AccountProfile,
            metadata:AccountMetadata,
            display_name:str|None=None,
            email:EmailStrings|None=None,
            country:Country|None=None
        ) -> None:
        changed = False
        if email is not None and email != target_profile.email:
            target_profile.set_email(email=email)
            changed = True
        if display_name is not None and display_name != target_profile.display_name:
            target_profile.set_display_name(display_name=display_name)
            changed = True
        if country is not None and country != target_profile.country:
            target_profile.set_country(country=country)
            changed = True
        if changed:
            metadata.update()

    @staticmethod
    def update_basic_settings(
        target_basic_settings:AccountBasicSettings,
        metadata:AccountMetadata,
        is_public:bool|None = None
    ) -> None:
        changed = False
        if is_public is not None and is_public != target_basic_settings.is_public:
            target_basic_settings.set_is_public(is_public=is_public)
            changed = True

        if changed:
            metadata.update()