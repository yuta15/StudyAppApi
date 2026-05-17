import logging
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from src.app.core.exceptions import DatabaseError, NetworkError, UnauthorizedError
from src.app.endpoints.deps.db import get_session
from src.app.infra.account import AccountIdentityReadRepository
from src.app.infra.token import FirebaseTokenVerifier
from src.app.service.interface.account import AccountIdentityReadInterface
from src.app.service.interface.identity import TokenVerifierInterface, TokenData


bearer_scheme = HTTPBearer(auto_error=False)


def get_token_verifier() -> TokenVerifierInterface:
    return FirebaseTokenVerifier()


def get_account_identity_reader(session: Session = Depends(get_session)) -> AccountIdentityReadInterface:
    return AccountIdentityReadRepository(session=session)


def get_account_identity(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    token_verifier: TokenVerifierInterface = Depends(get_token_verifier),
) -> TokenData:
    return _verify_token(credentials=credentials, token_verifier=token_verifier)


def get_current_principal_id(
    session: Session = Depends(get_session),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    token_verifier: TokenVerifierInterface = Depends(get_token_verifier),
    identity_reader: AccountIdentityReadInterface = Depends(get_account_identity_reader),
) -> UUID:
    token_data = _verify_token(credentials=credentials, token_verifier=token_verifier)
    return _resolve_principal_id(
        session=session,
        token_data=token_data,
        identity_reader=identity_reader,
    )


def get_optional_principal_id(
    session: Session = Depends(get_session),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    token_verifier: TokenVerifierInterface = Depends(get_token_verifier),
    identity_reader: AccountIdentityReadInterface = Depends(get_account_identity_reader),
) -> UUID | None:
    if credentials is None:
        return None

    token_data = _verify_token(credentials=credentials, token_verifier=token_verifier)
    return _resolve_principal_id(
        session=session,
        token_data=token_data,
        identity_reader=identity_reader,
    )


def _verify_token(
    credentials: HTTPAuthorizationCredentials | None,
    token_verifier: TokenVerifierInterface,
) -> TokenData:
    if not _has_bearer_credentials(credentials):
        raise _unauthorized_exception()

    try:
        return token_verifier.verify(raw_token=credentials.credentials)
    except UnauthorizedError as e:
        logging.error(e)
        raise _unauthorized_exception() from e


def _resolve_principal_id(
    session: Session,
    token_data: TokenData,
    identity_reader: AccountIdentityReadInterface,
) -> UUID:
    try:
        with session.begin():
            principal_id = identity_reader.resolve_principal_id(
                subject=token_data.subject,
                provider=token_data.provider,
            )
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


def _has_bearer_credentials(credentials: HTTPAuthorizationCredentials | None) -> bool:
    return credentials is not None and credentials.scheme.lower() == "bearer"


def _unauthorized_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized.",
        headers={"WWW-Authenticate": "Bearer"},
    )
