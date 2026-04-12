from dataclasses import dataclass
from src.app.model.account.entities.principals import Account
from src.app.model.account.entities.metadata import AccountMetadata
from src.app.model.account.entities.subjects import (
    AccountProfile,
    AccountBasicSettings, 
)


@dataclass
class DeleteAccountData:
    account:Account
    metadata:AccountMetadata
    profile:AccountProfile
    basic_settings:AccountBasicSettings


class DeleteAccountDomainService:
    @staticmethod
    def exec(delete_account_data:DeleteAccountData) -> None:
        delete_account_data.account.to_delete()
        delete_account_data.profile.delete()
        delete_account_data.basic_settings.delete()
        delete_account_data.metadata.delete()
        return