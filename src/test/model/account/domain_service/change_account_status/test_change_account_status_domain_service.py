import pytest

from src.app.model.account.entities.principals import AccountStatus
from src.app.model.account.service.change_account_status_domain_service import ChangeAccountStatusDomainService



def test_active_to_suspend_success(active_to_suspend):
    ChangeAccountStatusDomainService.exec(change_status_data=active_to_suspend)
    assert active_to_suspend.account.status == AccountStatus.SUSPENDED
    assert active_to_suspend.metadata.created_at != active_to_suspend.metadata.updated_at


def test_suspend_to_active_success(suspend_to_active):
    ChangeAccountStatusDomainService.exec(change_status_data=suspend_to_active)
    assert suspend_to_active.account.status == AccountStatus.ACTIVE
    assert suspend_to_active.metadata.created_at != suspend_to_active.metadata.updated_at


def test_active_to_deleted_failure(active_to_deleted):
    with pytest.raises(Exception):
        ChangeAccountStatusDomainService.exec(change_status_data=active_to_deleted)

def test_suspend_to_delete_failure(suspend_to_delete):
    with pytest.raises(Exception):
        ChangeAccountStatusDomainService.exec(change_status_data=suspend_to_delete)

def test_delete_to_active_failure(delete_to_active):
    with pytest.raises(Exception):
        ChangeAccountStatusDomainService.exec(change_status_data=delete_to_active)

def test_delete_to_suspend_failure(delete_to_suspend):
    with pytest.raises(Exception):
        ChangeAccountStatusDomainService.exec(change_status_data=delete_to_suspend)

def test_invalid_value_failure(invalid_value):
    with pytest.raises(Exception):
        ChangeAccountStatusDomainService.exec(change_status_data=invalid_value)
