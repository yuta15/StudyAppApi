from uuid import UUID

from src.app.service.authrization_service.models import AuthSubjectData, PrincipalData, TargetAuthorizationUnit
from src.app.service.authrization_service.principal_data_generator import PrincipalDataGenerator



class TargetAuthorizationUnitBuilder:
    """
    TargetAuthorizationUnitを構築するクラス。
    SubjectType毎に認可の対象となるPrincipal Dataを取得しPrincipalごとにTargetAuthorizationUnitの形に落とし込む。
    """
    def __init__(self, subject_principal_mapping:dict, principal_generator_mapping:dict):
        self.subject_principal_mapping = subject_principal_mapping
        self.principal_generator_mapping = principal_generator_mapping

    def build(self, account_id:UUID, auth_subject_data:AuthSubjectData) -> list[TargetAuthorizationUnit]:
        """
        全体を実行するパブリックメソッド
        """
        principal_data_generators = self._resolve_generators(auth_subject_data.subject_type)
        principal_data_list = self._run_generators(account_id=account_id, generators=principal_data_generators)
        return self._build_target_auth_unit_list(
            principal_data_list=principal_data_list,
            auth_subject_data=auth_subject_data
        )

    def _resolve_generators(self, subject_type) -> list[PrincipalDataGenerator]:
        """
        Subject毎に認可の対象となるPrincipalsを解決し、PrincipalDataを生成するクラスを返す
        """
        principal_types = self.subject_principal_mapping[subject_type]
        return [self.principal_generator_mapping[principal_type] for principal_type in principal_types]

    def _run_generators(self, account_id:UUID, generators:list[PrincipalDataGenerator]) -> list[PrincipalData]:
        """
        PrincipalDataを生成するための処理を順次実行する関数
        """
        principal_data_list = []
        for generator in generators:
            principal_data_list.extend(generator.create(account_id=account_id))
        return principal_data_list

    def _build_target_auth_unit_list(
            self, principal_data_list:list[PrincipalData], auth_subject_data:AuthSubjectData
        ) -> list[TargetAuthorizationUnit]:
        """
        TargetAuthorizationUnitをまとめて構築する
        """
        authorization_unit_list = []
        for principal_data in principal_data_list:
            authorization_unit_list.append(
                TargetAuthorizationUnit(
                    principal_id=principal_data.principal_id,
                    principal_type=principal_data.principal_type,
                    subject_id=auth_subject_data.subject_id,
                    subject_type=auth_subject_data.subject_type,
                    action=auth_subject_data.action
            ))
        return authorization_unit_list

