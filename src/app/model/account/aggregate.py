from dataclasses import dataclass
from typing import Self

from src.app.model.account.entities import Account, AccountMetadata
from src.app.model.account.account_subjects import AccountProfile, AccountBasicSettings, AccountAuthSettins


@dataclass
class AccountAggregate:
    account:Account
    metadata:AccountMetadata
    profile:AccountProfile
    basic_settings:AccountBasicSettings
    auth_settings:AccountAuthSettins

    @classmethod
    def new(cls, account_name:str, name:str, email:str, hashed_password:str, **kwargs) -> Self:
        account = Account.new(account_name=account_name)
        return AccountAggregate(
            account=account,
            metadata=AccountMetadata.new(principal_id=account.principal_id),
            profile=AccountProfile.new(principal_id=account.principal_id, name=name, email=email),
            basic_settings=AccountBasicSettings.new(principal_id=account.principal_id),
            auth_settings=AccountAuthSettins.new(principal_id=account.principal_id, hashed_password=hashed_password)
        )
    
    def to_active(self) -> None:
        self.account.to_active()
        self.metadata.update()

    def to_suspend(self) -> None:
        self.account.to_suspended()
        self.metadata.update()

    def to_delete(self) -> None:
        self.account.to_delete()
        self.metadata.delete()
        self.profile.delete()
        self.basic_settings.delete()
        self.auth_settings.delete()