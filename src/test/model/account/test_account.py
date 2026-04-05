from uuid import UUID

import pytest

from src.app.model.account.entities.principals import Account, AccountStatus


def test_account_new(account_name):
    account = Account.new(account_name=account_name)
    assert account.account_name == account_name
    assert account.status == AccountStatus.ACTIVE
    assert isinstance(account.principal_id, UUID)


def test_account_to_delete_success(account_name):
    account = Account.new(account_name=account_name)
    account.to_delete()
    assert account.status == AccountStatus.DELETED


def test_account_to_suspend_success(account_name):
    account = Account.new(account_name=account_name)
    account.to_suspended()
    assert account.status == AccountStatus.SUSPENDED


def test_account_to_active_success(account_name):
    account = Account.new(account_name=account_name)
    account.to_suspended()
    account.to_active()
    assert account.status == AccountStatus.ACTIVE


def test_account_to_delete_failure(account_name):
    account = Account.new(account_name=account_name)
    account.to_delete()
    with pytest.raises(Exception):
        account.to_delete()


def test_account_to_suspend_failure(account_name):
    account = Account.new(account_name=account_name)
    account.to_delete()
    with pytest.raises(Exception):
        account.to_suspended()


def test_account_to_active_failure(account_name):
    account = Account.new(account_name=account_name)
    account.to_delete()
    with pytest.raises(Exception):
        account.to_active()
