import time
from datetime import datetime
from uuid import UUID
from src.app.model.account.principals.account import Account, AccountStatus


# 初期化できるか
def test_new_user(display_name):
    account = Account.new(display_name=display_name)
    assert isinstance(account.principal_id, UUID)
    assert account.display_name == display_name
    assert account.status == AccountStatus.ACTIVE
    assert isinstance(account.metadata.created_at, datetime)
    assert isinstance(account.metadata.updated_at, datetime)

def test_to_delete(display_name):
    account = Account.new(display_name=display_name)
    account.to_delete()
    assert account.status == AccountStatus.DELETED
    assert account.metadata.created_at != account.metadata.updated_at

def test_to_suspend(display_name):
    account = Account.new(display_name=display_name)
    account.to_suspend()
    assert account.status == AccountStatus.SUSPENDED
    assert account.metadata.created_at != account.metadata.updated_at

def test_to_active(display_name):
    account = Account.new(display_name=display_name)
    account.to_suspend()
    account.to_active()
    assert account.status == AccountStatus.ACTIVE
    assert account.metadata.created_at != account.metadata.updated_at

def test_to_active_failed(display_name):
    account = Account.new(display_name=display_name)
    account.to_delete()
    account.to_active()
    assert account.status == AccountStatus.DELETED

def test_to_suspend_failed(display_name):
    account = Account.new(display_name=display_name)
    account.to_delete()
    account.to_suspend()
    assert account.status == AccountStatus.DELETED
