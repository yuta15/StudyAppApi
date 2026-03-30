from src.app.service.infra.hasher.password_hasher import BasePasswordHasher
from src.app.schemas.api.account.account_schema import CreateAccountInput
from src.app.model.account.principals.account import Account
from src.app.model.account.value_object.account_settings import BasicSettings, AuthSettings, Profile
from src.app.model.account.repository.account_repository import AccountRepository



class AccountInitializer:
    def __init__(self, password_hasher:BasePasswordHasher, account_repository:AccountRepository):
        self.password_hasher = password_hasher
        self.account_repository = account_repository

    def initialize(self, account_input:CreateAccountInput) -> Account:
        hashed_password = self.password_hasher.hash(account_input.password)

        account = Account.new(display_name=account_input.display_name)
        profile = Profile.new(account_id=account.principal_id, email=account_input.email)
        basic_settings = BasicSettings.new(account_id=account.principal_id)
        auth_settings = AuthSettings.new(account_id=account.principal_id, hashed_password=hashed_password)

        self.account_repository.sync_account(account)
        self.account_repository.sync_profile(profile)
        self.account_repository.sync_basic_settings(basic_settings)
        self.account_repository.sync_auth_settings(auth_settings)

        return account