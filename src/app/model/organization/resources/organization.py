from uuid import UUID
from dataclasses import dataclass

from src.app.model.base.resource import Resource
from src.app.model.organization.settings.organization_settings import OrganizationSettings


@dataclass
class Organization(Resource):
    settings:OrganizationSettings
    textbooks:list[UUID] = []
