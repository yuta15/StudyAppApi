from dataclasses import dataclass


@dataclass
class OrganizationBasicSettings:
    is_public:bool
    short_description:str


@dataclass
class OrganizationSettings:
    basic:OrganizationBasicSettings