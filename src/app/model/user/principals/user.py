from dataclasses import dataclass

from src.app.model.base.principal import Principal
from src.app.model.user.user_settings import UserSettings


@dataclass
class User(Principal):
    settings:UserSettings