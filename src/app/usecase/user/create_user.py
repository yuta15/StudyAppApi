from src.app.model.user.principals.user import User
from src.app.schemas.api.user.usre_schema import CreateUserInput, CreateUserOutput
from src.app.service.infra.hasher.password_hasher import PasswordHasher


class CreateUserUseCase:
    def __init__(self, user_repository, password_hasher:PasswordHasher):
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    def execute(self, session, create_user_input:CreateUserInput) -> CreateUserOutput:
        # TODO:重複とかはカスタムエラーを吐いてAPI層で409を返すようにする。
        # TODO: トランザクション境界をここで持ちたいけどSessionDepsとかでやっちゃうかもだからそうなったらもう一段上の層でやる。
        #       もしくはユースケース側でSessionを取れるようにしちゃった方がいけてるかも。
        hashed_password = self.password_hasher.hash(create_user_input.password)
        user = User.new(
            display_name=create_user_input.display_name,
            username=create_user_input.username,
            email=create_user_input.email,
            hashed_password=hashed_password
        )
        user = self.user_repository.create_user(user)
        return CreateUserOutput(id=user.id, display_name=user.display_name)