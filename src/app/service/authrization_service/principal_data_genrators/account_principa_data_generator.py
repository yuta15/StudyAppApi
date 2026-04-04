from uuid import UUID

from src.app.model.shared.entities import PrincipalTypes
from src.app.service.authrization_service.models import PrincipalData
from src.app.service.authrization_service.principal_data_generator import PrincipalDataGenerator


class AccoutPrincipalDataGenerator(PrincipalDataGenerator):
    def create(self, account_id:UUID) -> list[PrincipalData]:
        return [self._build_principal_data(principal_id=account_id, principal_type=PrincipalTypes.ACCOUNT)]