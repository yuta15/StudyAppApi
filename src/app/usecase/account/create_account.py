from sqlmodel import Session

from src.app.schemas.api.account.account_schema import CreateAccountInput, CreateAccountOutput
from src.app.service.account.account_initializer import AccountInitializer


class CreateUserUseCase:
    def __init__(self, session:Session, initializer:AccountInitializer):
        self.session = session
        self.initializer = initializer

    def execute(self, create_user_input:CreateAccountInput) -> CreateAccountOutput:
        # TODO:重複とかはカスタムエラーを吐いてAPI層で409を返すようにする。
        try:
            account = self.initializer.initialize(create_user_input)
        except Exception as e:
            self.session.rollback()
            raise Exception(e)
        else:
            self.session.commit()
            return CreateAccountOutput(id=account.principal_id, display_name=account.display_name)