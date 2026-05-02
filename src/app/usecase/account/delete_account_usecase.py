from uuid import UUID

from sqlmodel import Session
from src.app.model.account import DeleteAccountData, DeleteAccountDomainService
from src.app.usecase.account.repository import DeleteAccountRepositories
from src.app.service.authorization_service.account.account_auth_service import AccountAuthService


class DeleteAccountUsecase:
    def __init__(self, session: Session, repositories: DeleteAccountRepositories):
        self.session = session
        self.repositories = repositories

    def exec(self, principal_id: UUID) -> None:
        with self.session.begin():
            auth_service = AccountAuthService(repository=self.repositories.account_auth_read)
            auth_service.auth(principal_id=principal_id)

            account = self.repositories.account.get(principal_id=principal_id)
            metadata = self.repositories.metadata.get(principal_id=principal_id)
            profile = self.repositories.profile.get(principal_id=principal_id)
            basic_settings = self.repositories.basic_settings.get(principal_id=principal_id)
            identity = self.repositories.identity.get(principal_id=principal_id)

            delete_account_data = DeleteAccountData(
                account=account,
                metadata=metadata,
                profile=profile,
                basic_settings=basic_settings,
                identity=identity,
            )
            DeleteAccountDomainService.exec(delete_account_data=delete_account_data)

            self.repositories.account.save(account=account)
            self.repositories.metadata.save(metadata=metadata)
            self.repositories.profile.save(profile=profile)
            self.repositories.basic_settings.save(basic_settings=basic_settings)
            self.repositories.identity.save(identity=identity)
