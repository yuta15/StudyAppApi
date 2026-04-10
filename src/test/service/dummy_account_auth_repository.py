from src.app.service.authorization_service.account_auth_read_interface import AccountAuthReadInterface


class DummyAccuntAuthReader(AccountAuthReadInterface):        
    def __init__(self, result:bool):
        self.result = result
        self._called_args = {}

    def is_owned_subject(self, account_id, subject_type, subject_id) -> bool:
        self._called_args = {
            "account_id":account_id,
            "subject_type":subject_type,
            "subject_id":subject_id
        }
        return self.result
    