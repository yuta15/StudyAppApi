from src.app.service.authrization_service.models import TargetAuthorizationUnit
from src.app.service.authrization_service.authorization_checker import AuthorizationChecker
from src.app.model.account.account_subjects import AccountSubjcects


class AccountSubjectAuthorizationChecker(AuthorizationChecker):
    """
    AccountSubject用の認可処理を実装するクラス。
    AccountSubjectは所有者以外触れないため、マッチするものがない場合は権限なしとなる。
    """
    def __init__(self, repository):
        self.repository = repository

    def check(self, target:TargetAuthorizationUnit) -> bool:
        """"""
        # 所有者以外は触れないのでaccount_idとsubject_idの両方にマッチするProfileが存在する場合には権限ありとする。
        if not isinstance(target.subject_type, AccountSubjcects):
            raise ValueError("想定外のsubject_typeが入力されました。")

        subject = self.repository.find_subject_with_account_id(
            account_id=target.principal_id,
            subject_type=target.subject_type,
            subject_id=target.subject_id
        )
        if subject:
            return True
        return False