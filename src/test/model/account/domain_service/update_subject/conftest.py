import pytest


from src.app.model.account.service.update_subjects_domain_service import UpdateSubjectData


@pytest.fixture
def profile_update_subject(profile, metadata):
    return UpdateSubjectData(subject=profile, metadata=metadata)

@pytest.fixture
def basic_settings_update_subject(basic_settings, metadata):
    return UpdateSubjectData(subject=basic_settings, metadata=metadata)

@pytest.fixture
def auth_settings_update_subject(auth_settings, metadata):
    return UpdateSubjectData(subject=auth_settings, metadata=metadata)