import pytest

from src.app.model.account.entities.value_object import EmailStrings
from src.app.model.account.entities.subjects import Country
from src.app.model.account.service.update_subjects_domain_service import UpdateSubjectsDomainService


@pytest.mark.parametrize(
    "values",
    [
        {"display_name": "dummy_display_name"},
        {"email": EmailStrings("dummy@example.com")},
        {"country": Country.JP},
        {
            "display_name": "dummy_display_name",
            "email": EmailStrings("dummy@example.com"),
        },
        {"display_name": "dummy_display_name", "country": Country.JP},
        {"email": EmailStrings("dummy@example.com"), "country": Country.JP},
        {
            "display_name": "dummy_display_name",
            "email": EmailStrings("dummy@example.com"),
            "country": Country.JP,
        },
    ],
    ids=[
        "only_display_name",
        "only_email",
        "only_country",
        "display_name_and_email",
        "display_name_and_country",
        "email_and_country",
        "all",
    ],
)
def test_update_profile_success(profile_generator, metadata_generator, values):
    """
    profileが更新可能であることを確認する。
    単一・複数の値を入れた場合に適切に更新されていることをチェックする。
    """
    profile_data = profile_generator()
    metadata_data = metadata_generator()
    is_changed = UpdateSubjectsDomainService.update_profile(
        target_profile=profile_data, metadata=metadata_data, **values
    )
    for p, v in values.items():
        if p == "display_name":
            assert profile_data.display_name == v
        elif p == "email":
            assert profile_data.email == v
        elif p == "country":
            assert profile_data.country == v
    assert metadata_data.updated_at != metadata_data.created_at
    assert is_changed


def test_update_profile_no_change(profile_generator, metadata_generator):
    """
    変更せず、metadataも更新されないことをチェックする。
    """
    profile_data = profile_generator()
    metadata_data = metadata_generator()
    updated_at = metadata_data.updated_at
    display_name = profile_data.display_name
    email = profile_data.email
    country = profile_data.country
    is_changed = UpdateSubjectsDomainService.update_profile(target_profile=profile_data, metadata=metadata_data)
    assert not is_changed
    assert profile_data.display_name == display_name
    assert profile_data.email == email
    assert profile_data.country == country
    assert metadata_data.updated_at == updated_at


@pytest.mark.parametrize("values", [{"is_public": False}])
def test_update_basic_settings_success(basic_settings_generator, metadata_generator, values):
    """
    basic_settingsの更新可能であることをチェックする。
    想定通り更新されることをチェックする。
    """
    basic_settings_data = basic_settings_generator()
    metadata_data = metadata_generator()
    updated_at = metadata_data.updated_at
    is_changed = UpdateSubjectsDomainService.update_basic_settings(
        target_basic_settings=basic_settings_data, metadata=metadata_data, **values
    )
    for k, v in values.items():
        if k == "is_public":
            assert basic_settings_data.is_public == v
    assert is_changed
    assert metadata_data.updated_at != updated_at


def test_update_basic_settings_no_change(basic_settings_generator, metadata_generator):
    basic_settings_data = basic_settings_generator()
    metadata_data = metadata_generator()
    is_public = basic_settings_data.is_public
    is_changed = UpdateSubjectsDomainService.update_basic_settings(
        target_basic_settings=basic_settings_data, metadata=metadata_data
    )
    assert not is_changed
    assert basic_settings_data.is_public == is_public
    assert metadata_data.updated_at == metadata_data.created_at
