from uuid import UUID
from dataclasses import dataclass

from src.app.model.base.principal import Principal
from src.app.model.organization.settings.group_settings import GroupSettings


@dataclass
class Group(Principal):
    settings:GroupSettings
    user_ids:list[UUID] = []