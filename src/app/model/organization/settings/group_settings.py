from dataclasses import dataclass


@dataclass
class GroupBasicSettings:
    description:str


@dataclass
class GroupSettings:
    basic:GroupBasicSettings