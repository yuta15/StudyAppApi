from datetime import datetime
from uuid import UUID

from src.app.model.account.entities.metadata import AccountMetadata


def test_account_metadata_new(account_principal_id):
    metadata = AccountMetadata.new(principal_id=account_principal_id)
    assert metadata.principal_id == account_principal_id
    assert isinstance(metadata.metadata_id, UUID)
    assert isinstance(metadata.created_at, datetime)
    assert isinstance(metadata.updated_at, datetime)
    assert metadata.deleted_at == None


def test_account_metadata_update(metadata_generator):
    metadata = metadata_generator()
    metadata.update()
    assert metadata.created_at != metadata.updated_at

def test_account_metadata_delete(metadata_generator):
    metadata = metadata_generator()
    metadata.delete()
    assert isinstance(metadata.deleted_at, datetime)
