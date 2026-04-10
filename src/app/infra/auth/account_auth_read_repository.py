from src.app.service.authorization_service.account_auth_read_interface import AccountAuthReadInterface


class AccountAuthReadRepository(AccountAuthReadInterface):
    def __init__(self, db_operator):
        self.db_operator = db_operator

    def is_owned_subject(self, account_id, subject_type, subject_id):...
        