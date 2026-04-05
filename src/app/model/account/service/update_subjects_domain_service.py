from src.app.model.account.entities.metadata import AccountMetadata
from src.app.model.account.entities.subjects import (
    Country,
    AccountSubject,
    AccountProfile,
    AccountBasicSettings, 
    AccountAuthSettins
)


class UpdateSubjectData:
    subject:AccountSubject
    metadata:AccountMetadata


class UpdateSubjectsDomainService:
    def update_profile(
            self,
            update_subject_data:UpdateSubjectData,
            display_name:str|None=None,
            email:str|None=None,
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

    def update_basic_settings(self, update_subject_data:UpdateSubjectData, is_public:bool|None = None) -> None:
        if not isinstance(update_subject_data.subject, AccountBasicSettings):
            raise ValueError("異なるデータが入っているよ")

        changed = False
        if is_public is not None and is_public != update_subject_data.subject.is_public:
            update_subject_data.subject.set_is_public(is_public=is_public)
            changed = True

        if changed:
            update_subject_data.metadata.update()

    def update_auth_settings(self, update_subject_data:UpdateSubjectData, hashed_password:str|None = None) -> None:
        if not isinstance(update_subject_data.subject, AccountAuthSettins):
            raise ValueError("異なるデータが入っているよ")
        
        changed = False
        if hashed_password is not None and hashed_password != update_subject_data.subject.hashed_password:
            update_subject_data.subject.set_hashed_password(is_public=hashed_password)
            changed = True

        if changed:
            update_subject_data.metadata.update()
