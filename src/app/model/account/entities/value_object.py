import re
from dataclasses import dataclass


@dataclass(frozen=True)
class AccountNameStrings:
    value: str

    def __post_init__(self):
        self._check_regex(value=self.value)
        self._check_length(value=self.value)

    @staticmethod
    def _check_regex(value: str) -> bool:
        if re.fullmatch(r"^[a-zA-Z0-9-_]+$", value) is None:
            AccountNameStrings._raise_invalid_value(value=value)

    @staticmethod
    def _check_length(value: str) -> bool:
        MIN_LENGTH = 3
        MAX_LENGTH = 25
        if not MIN_LENGTH < len(value) <= MAX_LENGTH:
            AccountNameStrings._raise_invalid_value(value=value)

    @staticmethod
    def _raise_invalid_value(value) -> None:
        raise ValueError(f"invalid account name. value:{value}")


@dataclass(frozen=True)
class EmailStrings:
    value: str

    def __post_init__(self):
        if "@" not in self.value:
            raise ValueError("invalid email")
