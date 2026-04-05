from src.app.model.account.account_subjects import AccountSubjcects
from src.app.model.shared.entities import PrincipalTypes
from src.app.service.authrization_service.principal_data_genrators.account_principa_data_generator import AccoutPrincipalDataGenerator



subject_principal_mapping = {
    AccountSubjcects.ACCOUNT_PROFILE: [PrincipalTypes.ACCOUNT],
    AccountSubjcects.ACCOUNT_AUTH_SETTINGS: [PrincipalTypes.ACCOUNT],
    AccountSubjcects.ACCOUNT_BASIC_SETTINGS: [PrincipalTypes.ACCOUNT]
}


principal_generator_provider_mappings = {
    PrincipalTypes.ACCOUNT: lambda: AccoutPrincipalDataGenerator()
}


subject_check_service_provider = {
    AccountSubjcects.ACCOUNT_PROFILE: [PrincipalTypes.ACCOUNT],
    AccountSubjcects.ACCOUNT_AUTH_SETTINGS: [PrincipalTypes.ACCOUNT],
    AccountSubjcects.ACCOUNT_BASIC_SETTINGS: [PrincipalTypes.ACCOUNT]
}