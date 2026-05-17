from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from src.app.core.exceptions import DatabaseError, NetworkError, UnauthorizedError
from src.app.endpoints.deps.db import get_session
from src.app.infra.account import AccountIdentityReadRepository
from src.app.infra.token import FirebaseTokenVerifier
from src.app.service.interface.account import AccountIdentityReadInterface
from src.app.service.interface.identity import TokenVerifierInterface


bearer_scheme = HTTPBearer(auto_error=False)


def get_token_verifier() -> TokenVerifierInterface:
    return FirebaseTokenVerifier()


def get_account_identity_reader(
    session: Session = Depends(get_session),
) -> AccountIdentityReadInterface:
    return AccountIdentityReadRepository(session=session)


def get_current_principal_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    token_verifier: TokenVerifierInterface = Depends(get_token_verifier),
    identity_reader: AccountIdentityReadInterface = Depends(get_account_identity_reader),
) -> UUID:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise _unauthorized_exception()

    try:
        token_data = token_verifier.verify(raw_token=credentials.credentials)
        principal_id = identity_reader.resolve_principal_id(
            subject=token_data.subject,
            provider=token_data.provider,
        )
    except UnauthorizedError as e:
        raise _unauthorized_exception() from e
    except NetworkError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication unavailable.",
        ) from e
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error.",
        ) from e

    if principal_id is None:
        raise _unauthorized_exception()
    return principal_id


def get_optional_principal_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    token_verifier: TokenVerifierInterface = Depends(get_token_verifier),
    identity_reader: AccountIdentityReadInterface = Depends(get_account_identity_reader),
) -> UUID | None:
    if credentials is None:
        return None
    return get_current_principal_id(
        credentials=credentials,
        token_verifier=token_verifier,
        identity_reader=identity_reader,
    )


def _unauthorized_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized.",
        headers={"WWW-Authenticate": "Bearer"},
    )
