from dataclasses import dataclass

from src.app.model.account import AllowedIdentityProvider


@dataclass(frozen=True)
class TokenData:
    subject: str
    provider: AllowedIdentityProvider
