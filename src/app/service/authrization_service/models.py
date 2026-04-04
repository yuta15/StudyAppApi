from enum import Enum
from uuid import UUID
from dataclasses import dataclass

from src.app.model.shared.entities import PrincipalTypes


@dataclass
class AuthSubjectData:
    subject_id:UUID
    subject_type:Enum
    action:Enum


@dataclass
class PrincipalData:
    principal_id:UUID
    principal_type:PrincipalTypes


@dataclass
class TargetAuthorizationUnit:
    principal_id:UUID
    principal_type:PrincipalTypes
    subject_id:UUID
    subject_type:Enum
    action:Enum