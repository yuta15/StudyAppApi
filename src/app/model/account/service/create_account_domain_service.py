from dataclasses import dataclass

from src.app.model.account import (
    Account,
    AccountBasicSettings,
    AccountIdentity,
    AccountMetadata,
    AccountNameStrings,
    AccountProfile,
    AllowedIdentityProvider,
    EmailStrings,
)


@dataclass
class CreateAccountInput:
    account_name: AccountNameStrings
    display_name: str
    email: EmailStrings
    subject: str
    provider: AllowedIdentityProvider


@dataclass
class CreateAccountOutput:
    account: Account
    metadata: AccountMetadata
    profile: AccountProfile
    basic_settings: AccountBasicSettings
    identity: AccountIdentity


class CreateAccountDomainService:
    @staticmethod
    def exec(create_account_input: CreateAccountInput) -> CreateAccountOutput:
        account = Account.new(account_name=create_account_input.account_name)
        return CreateAccountOutput(
            account=account,
            metadata=AccountMetadata.new(principal_id=account.principal_id),
            profile=AccountProfile.new(
                principal_id=account.principal_id,
                display_name=create_account_input.display_name,
                email=create_account_input.email,
            ),
            basic_settings=AccountBasicSettings.new(principal_id=account.principal_id),
            identity=AccountIdentity.new(
                principal_id=account.principal_id,
                subject=create_account_input.subject,
                provider=create_account_input.provider,
            ),
        )
