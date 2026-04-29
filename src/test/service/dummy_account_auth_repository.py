from src.app.service.authorization_service.account.account_auth_read_interface import AccountAuthReadInterface


class TestAccountAuthReaderException(Exception):
    """ダミーのエラー"""


class DummyAccuntAuthReader(AccountAuthReadInterface):
    def __init__(self, result, is_negative: bool = False):
        self._result = result
        self._is_negative = is_negative
        self._input_principal_id = None

    def has_specified_active_user(self, principal_id):
        self._input_principal_id = principal_id
        if self._is_negative:
            raise TestAccountAuthReaderException()
        return self._result
