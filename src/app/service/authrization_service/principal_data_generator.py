from uuid import UUID
from abc import ABC, abstractmethod

from src.app.model.shared.entities import PrincipalTypes
from src.app.service.authrization_service.models import PrincipalData


class PrincipalDataGenerator(ABC):
    """
    PrincipalDataを生成する処理を書く基底クラス。
    Account IDから各PrincipalのPrincipalDataを生成する具体的な処理はこのクラスを継承して実装する。
    Mappingし忘れると呼び出されないので注意。
    具体実装は`principal_data_genrator`に格納すること
    """
    @abstractmethod
    def create(self, account_id:UUID) -> list[PrincipalData]:...

    def _build_principal_data(self, principal_id:UUID, principal_type:PrincipalTypes) -> PrincipalData:
        return PrincipalData(principal_id=principal_id, principal_type=principal_type)