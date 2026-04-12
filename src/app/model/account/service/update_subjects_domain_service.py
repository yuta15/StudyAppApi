from dataclasses import dataclass

from src.app.model.account.entities.value_object import EmailStrings
from src.app.model.account.entities.metadata import AccountMetadata
from src.app.model.account.entities.subjects import (
    Country,
    AccountSubject,
    AccountProfile,
    AccountBasicSettings,
)


@dataclass
class UpdateSubjectData:
    subject:AccountSubject
    metadata:AccountMetadata


class UpdateSubjectsDomainService:
    @staticmethod
    def update_profile(
            update_subject_data:UpdateSubjectData,
            display_name:str|None=None,
            email:EmailStrings|None=None,
            country:Country|None=None
        ) -> None:
        if not isinstance(update_subject_data.subject, AccountProfile):
            raise ValueError("異なるデータが入っているよ")

        changed = False
        if email is not None and email != update_subject_data.subject.email:
            update_subject_data.subject.set_email(email=email)
            changed = True
        if display_name is not None and display_name != update_subject_data.subject.display_name:
            update_subject_data.subject.set_display_name(display_name=display_name)
            changed = True
        if country is not None and country != update_subject_data.subject.country:
            update_subject_data.subject.set_country(country=country)
            changed = True
        if changed:
            update_subject_data.metadata.update()

    @staticmethod
    def update_basic_settings(update_subject_data:UpdateSubjectData, is_public:bool|None = None) -> None:
        if not isinstance(update_subject_data.subject, AccountBasicSettings):
            raise ValueError("異なるデータが入っているよ")

        changed = False
        if is_public is not None and is_public != update_subject_data.subject.is_public:
            update_subject_data.subject.set_is_public(is_public=is_public)
            changed = True

        if changed:
            update_subject_data.metadata.update()