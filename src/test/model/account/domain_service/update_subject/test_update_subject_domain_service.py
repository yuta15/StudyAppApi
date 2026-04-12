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
            {"display_name": "dummy_display_name", "email": EmailStrings("dummy@example.com")},
            {"display_name": "dummy_display_name", "country": Country.JP},
            {"email": EmailStrings("dummy@example.com"), "country": Country.JP},
            {"display_name": "dummy_display_name", "email": EmailStrings("dummy@example.com"), "country": Country.JP},
        ],
        ids=[
            "only_display_name",
            "only_email",
            "only_country",
            "display_name_and_email",
            "display_name_and_country",
            "email_and_country",
            "all",
        ]

)
def test_update_profile_success(profile, metadata, values):
    """
    profileが更新可能であることを確認する。
    単一・複数の値を入れた場合に適切に更新されていることをチェックする。
    """
    UpdateSubjectsDomainService.update_profile(target_profile=profile, metadata=metadata, **values)
    for p, v in values.items():
        if p == "display_name":
            assert profile.display_name == v
        elif p == "email":
            assert profile.email == v
        elif p == "country":
            assert profile.country == v
    assert metadata.updated_at != metadata.created_at


def test_update_profile_no_change(profile, metadata):
    """
    変更せず、metadataも更新されないことをチェックする。
    """
    display_name = profile.display_name
    email = profile.email
    country = profile.country
    UpdateSubjectsDomainService.update_profile(target_profile=profile, metadata=metadata)
    assert profile.display_name == display_name
    assert profile.email == email
    assert profile.country == country
    assert metadata.updated_at == metadata.created_at


def test_update_profile_invalid_subject(basic_settings, metadata):
    """
    不正なsubjectを入力した場合にValueErrorが発生することをチェックする。
    """
    with pytest.raises(ValueError):
        UpdateSubjectsDomainService.update_profile(target_profile=basic_settings, metadata=metadata)


@pytest.mark.parametrize(
        "values",
        [
            {"is_public": False}
        ]
)
def test_update_basic_settings_success(basic_settings, metadata, values):
    """
    basic_settingsの更新可能であることをチェックする。
    想定通り更新されることをチェックする。
    """
    UpdateSubjectsDomainService.update_basic_settings(target_basic_settings=basic_settings, metadata=metadata, **values)
    for k, v in values.items():
        if k == "is_public":
            assert basic_settings.is_public == v
    assert metadata.updated_at != metadata.created_at


def test_update_basic_settings_no_change(basic_settings, metadata):
    is_public = basic_settings.is_public
    UpdateSubjectsDomainService.update_basic_settings(target_basic_settings=basic_settings, metadata=metadata)
    assert basic_settings.is_public == is_public
    assert metadata.updated_at == metadata.created_at


def test_update_basic_settings_invalid_subject_failure(profile, metadata):
    """
    不正なsubjectを入力した場合にValueErrorが発生することをチェックする。
    """
    with pytest.raises(ValueError):
        UpdateSubjectsDomainService.update_basic_settings(target_basic_settings=profile, metadata=metadata)