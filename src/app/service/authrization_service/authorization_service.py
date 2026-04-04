from uuid import UUID

from src.app.service.authrization_service.target_authorization_unit_builder import TargetAuthorizationUnitBuilder
from src.app.service.authrization_service.authorization_checker import AuthorizationChecker
from src.app.service.authrization_service.models import AuthSubjectData


class AuthorizationService:
    """
    認可サービス。
    account_Idが特定のリソースに対する操作を許可されているかを判定する。
    このクラスはUseCaseから呼び出されることを想定しており、SubjectDataに指定したsubjectに対する操作を判定する処理を流す。
    リソースに応じてaccount_idのみの認可をチェックするか、groupを含めて判断するかが異なるため、解決した上でチェックする。
    """
    def __init__(self, subject_principal_mapping, principal_generator_mapping, checker_mapping):
        self.builder = TargetAuthorizationUnitBuilder(subject_principal_mapping, principal_generator_mapping)
        self.checker_mapping = checker_mapping

    def is_authorized(self, account_id:UUID, auth_subject_data_list:list[AuthSubjectData]):
        target_list = []
        for auth_subject_data in auth_subject_data_list:
            target_list.extend(self.builder.build(account_id=account_id, auth_subject_data=auth_subject_data))

        for target in target_list:
            checker = self.checker_mapping[target.subject_type]
            if not checker.check(target):
                return False
        return True
