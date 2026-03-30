from uuid import UUID
from dataclasses import dataclass


@dataclass
class Principal:
    principal_id:UUID
    display_name:str