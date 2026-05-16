from dataclasses import dataclass

from src.app.model.account import (
    Account,
    AccountBasicSettings,
    AccountMetadata,
    AccountProfile,
)


@dataclass
class DeleteAccountData:
    account: Account
    metadata: AccountMetadata
    profile: AccountProfile
    basic_settings: AccountBasicSettings


class DeleteAccountDomainService:
    @staticmethod
    def exec(delete_account_data: DeleteAccountData) -> None:
        delete_account_data.account.to_delete()
        delete_account_data.profile.delete()
        delete_account_data.basic_settings.delete()
        delete_account_data.metadata.delete()
        return
