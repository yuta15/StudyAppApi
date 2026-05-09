from src.app.core.exceptions import UnauthorizedError
from src.app.model.textbook import TextbookStatus
from src.app.service.authorization_service.textbook import TextbookAuthReadInterface
from src.app.service.domain_read_service.interface.textbook import TextbookVisibility


class DummyAccountAuthService:
    def __init__(self, is_authorized: bool):
        self._is_authorized = is_authorized
        self._input_principal_id = None

    def auth(self, principal_id):
        self._input_principal_id = principal_id
        if not self._is_authorized:
            raise UnauthorizedError(
                msg=f"Unauthorized Error principal_id:{principal_id}",
                principal_id=principal_id,
            )


class DummyTextbookAuthReader(TextbookAuthReadInterface):
    def __init__(
        self,
        result: bool,
        is_public: bool = True,
        status: TextbookStatus = TextbookStatus.DRAFT,
    ):
        self._result = result
        self._is_public = is_public
        self._status = status
        self._input_principal_id = None
        self._input_textbook_id = None
        self._input_visibility_textbook_id = None

    def is_author(self, principal_id, textbook_id):
        self._input_principal_id = principal_id
        self._input_textbook_id = textbook_id
        return self._result

    def fetch_textbook_visibility(self, textbook_id):
        self._input_visibility_textbook_id = textbook_id
        return TextbookVisibility(
            textbook_id=textbook_id,
            status=self._status,
            is_public=self._is_public,
        )
