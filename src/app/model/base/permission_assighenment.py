from uuid import UUID
from dataclasses import dataclass

from app.model.base.enum import PrincipalTypes


@dataclass
class PermissionAssighenment:
    id:UUID
    permission_definition_id:UUID
    resource_id:UUID
    princilpal_id:UUID
    principal_type:PrincipalTypes
    
