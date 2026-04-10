from uuid import UUID

from src.app.usecase.account.models import CreateAccountDTO


class CreateAccountUsecase:
    def __init__(self, session, repository):
        self.session = session
        self.repository = repository

    def exec(self, create_account_dto:CreateAccountDTO) -> UUID:...