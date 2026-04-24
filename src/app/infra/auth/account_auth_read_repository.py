from uuid import UUID

from src.app.service.authorization_service.account_auth_read_interface import AccountAuthReadInterface


class AccountAuthReadRepository(AccountAuthReadInterface):
    def __init__(self, db_operator):
        self.db_operator = db_operator

    def has_specified_active_user(self, principal_id:UUID):...
        
