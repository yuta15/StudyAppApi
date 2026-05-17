from uuid import UUID

from sqlmodel import Session

from src.app.service.authorization_service.account import AccountAuthService
from src.app.usecase.account.dto import AccountOutputDTO, OutputMetadata, OutputProfile, OutputSettings
from src.app.usecase.account.repository import GetAccountRepositories


class GetAccountUsecase:
    def __init__(self, session: Session, repositories: GetAccountRepositories):
        self.session = session
        self.repositories = repositories

    def exec(self, principal_id: UUID) -> AccountOutputDTO:
        with self.session.begin():
            auth_service = AccountAuthService(repository=self.repositories.account_auth_read)
            auth_service.auth(principal_id=principal_id)

            account = self.repositories.account.get(principal_id=principal_id)
            metadata = self.repositories.metadata.get(principal_id=principal_id)
            profile = self.repositories.profile.get(principal_id=principal_id)
            basic_settings = self.repositories.basic_settings.get(principal_id=principal_id)

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
