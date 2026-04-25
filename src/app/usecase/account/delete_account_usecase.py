from uuid import UUID

from sqlmodel import Session
from src.app.usecase.account.models import DeleteAccountRepositories
from src.app.service.authorization_service.account_auth_service import AccountAuthService
from src.app.model.account.service.delete_account_domain_service import DeleteAccountData, DeleteAccountDomainService


class DeleteAccountUsecase:
    def __init__(self, session:Session, repositories:DeleteAccountRepositories):
        self.session = session
        self.repositories = repositories

    def exec(self, principal_id:UUID) -> None:
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
            identity=identity
        )
        DeleteAccountDomainService.exec(delete_account_data=delete_account_data)

        with self.session.begin():
            self.repositories.account.save(account=account)
            self.repositories.metadata.save(metadata=metadata)
            self.repositories.profile.save(profile=profile)
            self.repositories.basic_settings.save(basic_settings=basic_settings)
            self.repositories.identity.save(identity=identity)