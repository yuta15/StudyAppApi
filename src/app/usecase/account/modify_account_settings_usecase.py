from sqlmodel import Session

from src.app.model.account import UpdateSubjectsDomainService
from src.app.service.authorization_service.account import AccountAuthService
from src.app.usecase.account.repository import ModifyAccountRepositories
from src.app.usecase.account.dto import (
    ModifyAccountDTO,
    AccountOutputDTO,
    OutputProfile,
    OutputMetadata,
    OutputSettings,
)


class ModifyAccountSettingsUsecase:
    def __init__(self, session: Session, repositories: ModifyAccountRepositories):
        self.session = session
        self.repositories = repositories

    def exec(self, modify_account_dto: ModifyAccountDTO) -> AccountOutputDTO:
        with self.session.begin():
            # Auth
            auth_service = AccountAuthService(repository=self.repositories.account_auth_read)
            auth_service.auth(principal_id=modify_account_dto.principal_id)

            # 現在の設定をフェッチ
            account = self.repositories.account.get(principal_id=modify_account_dto.principal_id)
            metadata = self.repositories.metadata.get(principal_id=modify_account_dto.principal_id)
            profile = self.repositories.profile.get(principal_id=modify_account_dto.principal_id)
            basic_settings = self.repositories.basic_settings.get(principal_id=modify_account_dto.principal_id)

            # domain serviceの呼び出し
            basic_settings_changed = UpdateSubjectsDomainService.update_basic_settings(
                target_basic_settings=basic_settings,
                metadata=metadata,
                is_public=modify_account_dto.basic_settings.is_public,
            )
            profile_changed = UpdateSubjectsDomainService.update_profile(
                target_profile=profile,
                metadata=metadata,
                display_name=modify_account_dto.profile.display_name,
                email=modify_account_dto.profile.email,
                country=modify_account_dto.profile.country,
            )

            if basic_settings_changed:
                self.repositories.basic_settings.save(basic_settings=basic_settings)
            if profile_changed:
                self.repositories.profile.save(profile=profile)
            if basic_settings_changed or profile_changed:
                self.repositories.metadata.save(metadata=metadata)

            # ReadAccountの形に整形する。
            return AccountOutputDTO(
                principal_id=account.principal_id,
                account_name=account.account_name,
                status=account.status,
                metadata=OutputMetadata(created_at=metadata.created_at, last_update=metadata.updated_at),
                profile=OutputProfile(
                    display_name=profile.display_name,
                    email=profile.email,
                    country=profile.country,
                ),
                settings=OutputSettings(is_public=basic_settings.is_public),
            )
