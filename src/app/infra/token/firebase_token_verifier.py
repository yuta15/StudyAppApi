from firebase_admin import App, auth

from src.app.core.exceptions import NetworkError, UnauthorizedError
from src.app.model.account import AllowedIdentityProvider
from src.app.service.interface.identity import TokenData, TokenVerifierInterface


class FirebaseTokenVerifier(TokenVerifierInterface):
    def __init__(self, app: App | None = None, check_revoked: bool = False):
        self._app = app
        self._check_revoked = check_revoked

    def verify(self, raw_token: str) -> TokenData:
        try:
            decoded_token = auth.verify_id_token(
                id_token=raw_token,
                app=self._app,
                check_revoked=self._check_revoked,
            )
        except (
            ValueError,
            auth.InvalidIdTokenError,
            auth.ExpiredIdTokenError,
            auth.RevokedIdTokenError,
            auth.UserDisabledError,
        ) as e:
            raise UnauthorizedError("Invalid Firebase ID token.") from e
        except auth.CertificateFetchError as e:
            raise NetworkError(f"Failed to fetch Firebase public key certificates. {e}") from e

        return TokenData(
            subject=decoded_token["uid"],
            provider=AllowedIdentityProvider.FIREBASE,
        )
