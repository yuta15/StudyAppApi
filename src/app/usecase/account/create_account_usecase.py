from uuid import UUID

from sqlmodel import Session
from src.app.usecase.account.dto import CreateAccountDTO
from src.app.usecase.account.repository import  CreateAccountRepositories
from src.app.model.account.service.create_account_domain_service import CreateAccountDomainService, CreateAccountInput


class CreateAccountUsecase:
    def __init__(self, session:Session, repositories:CreateAccountRepositories):
        self.session = session
        self.repositories = repositories

    def exec(self, create_account_dto:CreateAccountDTO) -> UUID:
        output = CreateAccountDomainService.exec(create_account_input=CreateAccountInput(
            account_name=create_account_dto.account_name,
            display_name=create_account_dto.display_name,
            email=create_account_dto.email,
            subject=create_account_dto.subject,
            provider=create_account_dto.provider
        ))

        with self.session.begin():
            self.repositories.account.save(output.account)
            self.repositories.metadata.save(output.metadata)
            self.repositories.profile.save(output.profile)
            self.repositories.basic_settings.save(output.basic_settings)
            self.repositories.identity.save(output.identity)

        return output.account.principal_id