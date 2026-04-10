from src.app.service.authorization_service.models import AccountAuthInput
from src.app.service.authorization_service.auth_service_base import AuthServiceBase
from src.app.service.authorization_service.account_auth_read_interface import AccountAuthReadInterface


class AccountAuthService(AuthServiceBase[AccountAuthInput]):
    def __init__(self, repository:AccountAuthReadInterface):
        self.repository = repository

    def is_allowed(self, account_auth_input:AccountAuthInput) -> bool:
        return self.repository.is_owned_subject(
            account_id=account_auth_input.principal_id,
            subject_type=account_auth_input.subject_type,
            subject_id=account_auth_input.subject_id
        )
