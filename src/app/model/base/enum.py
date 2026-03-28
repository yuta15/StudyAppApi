from enum import Enum


class Country(Enum):
    JP = "JP"
    US = "US"
    CA = "CA"
    GB = "GB"
    DE = "DE"
    FR = "FR"
    IN = "IN"
    CN = "CN"
    KR = "KR"
    SG = "SG"
    AU = "AU"
    BR = "BR"


class ResourceTypes(Enum):
    ORGANIZATION = "Organization"
    TEXTBOOK = "Textbook"


class PrincipalTypes(Enum):
    USER = "User"
    GROUP = "GROUP"


class PermissionActions(Enum):
    CREATE = "CREATE"
    DELETE = "DELETE"
    MODIFY = "MODIFY"
    INVITE = "INVITE"