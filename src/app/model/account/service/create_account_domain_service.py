from dataclasses import dataclass

from src.app.model.account.entities.value_object import EmailStrings, AccountNameStrings
from src.app.model.account.entities.principals import Account
from src.app.model.account.entities.metadata import AccountMetadata
from src.app.model.account.entities.subjects import (
    AccountProfile,
    AccountBasicSettings, 
    AccountAuthSettings
)


@dataclass
class CreateAccountResults:
    account:Account
    metadata:AccountMetadata
    profile:AccountProfile
    basic_settings:AccountBasicSettings
    auth_settings:AccountAuthSettings


class CreateAccountDomainService:
    @staticmethod
    def exec(account_name:AccountNameStrings, display_name:str, email:EmailStrings, hashed_password:str) -> CreateAccountResults:
        account = Account.new(account_name=account_name)
        return CreateAccountResults(
            account=account,
            metadata=AccountMetadata.new(principal_id=account.principal_id),
            profile=AccountProfile.new(principal_id=account.principal_id, display_name=display_name, email=email),
            basic_settings=AccountBasicSettings.new(principal_id=account.principal_id),
            auth_settings=AccountAuthSettings.new(principal_id=account.principal_id, hashed_password=hashed_password)
        )