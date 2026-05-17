from uuid import UUID

from sqlalchemy.exc import IntegrityError, OperationalError, TimeoutError
from sqlmodel import Session, select

from src.app.core.exceptions import DatabaseError, DataNotFoundError, InvalidDataError, NetworkError
from src.app.model.account import AccountMetadata, AccountMetadataRepositoryInterface
from src.app.schemas.db.account import AccountMetadataTable


class AccountMetadataRepository(AccountMetadataRepositoryInterface):
    def __init__(self, session: Session):
        self._session = session

    def save(self, metadata: AccountMetadata) -> AccountMetadata:
        try:
            metadata_table = self._get_metadata(principal_id=metadata.principal_id)
            if metadata_table:
                metadata_table.created_at = metadata.created_at
                metadata_table.updated_at = metadata.updated_at
                metadata_table.deleted_at = metadata.deleted_at
            else:
                self._session.add(AccountMetadataTable.from_metadata(metadata=metadata))
            return metadata
        except IntegrityError as e:
            raise InvalidDataError(f"Invalid data error {e}")
        except (OperationalError, TimeoutError) as e:
            raise NetworkError(f"Connection failed. {e}")
        except Exception as e:
            raise DatabaseError(f"Unknown error. {e}")

    def get(self, principal_id: UUID) -> AccountMetadata:
        try:
            metadata_table = self._get_metadata(principal_id=principal_id)
        except (OperationalError, TimeoutError) as e:
            raise NetworkError(f"Connection failed. {e}")
        except Exception as e:
            raise DatabaseError(f"Unknown error. {e}")

        if metadata_table is None:
            raise DataNotFoundError("Account metadata not found.")
        return metadata_table.to_metadata()

    def _get_metadata(self, principal_id: UUID) -> AccountMetadataTable | None:
        stmt = select(AccountMetadataTable).where(AccountMetadataTable.principal_id == principal_id)
        return self._session.exec(statement=stmt).one_or_none()
