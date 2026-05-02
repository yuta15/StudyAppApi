from dataclasses import dataclass

from src.app.model.account import (
    Account,
    AccountBasicSettings,
    AccountIdentity,
    AccountMetadata,
    AccountProfile,
)


@dataclass
class DeleteAccountData:
    account: Account
    metadata: AccountMetadata
    profile: AccountProfile
    basic_settings: AccountBasicSettings
    identity: AccountIdentity


class DeleteAccountDomainService:
    @staticmethod
    def exec(delete_account_data: DeleteAccountData) -> None:
        delete_account_data.account.to_delete()
        delete_account_data.profile.delete()
        delete_account_data.basic_settings.delete()
        delete_account_data.metadata.delete()
        delete_account_data.identity.delete()
        return
