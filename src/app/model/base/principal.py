from uuid import UUID
from dataclasses import dataclass


@dataclass
class Principal:
    id:UUID
    display_name:str