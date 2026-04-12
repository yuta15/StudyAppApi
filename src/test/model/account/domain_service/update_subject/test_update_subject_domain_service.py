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
def test_update_profile_success(profile_update_subject, values):
    """
    profileが更新可能であることを確認する。
    単一・複数の値を入れた場合に適切に更新されていることをチェックする。
    """
    UpdateSubjectsDomainService.update_profile(update_subject_data=profile_update_subject, **values)
    for p, v in values.items():
        if p == "display_name":
            assert profile_update_subject.subject.display_name == v
        elif p == "email":
            assert profile_update_subject.subject.email == v
        elif p == "country":
            assert profile_update_subject.subject.country == v
    assert profile_update_subject.metadata.updated_at != profile_update_subject.metadata.created_at


def test_update_profile_no_change(profile_update_subject):
    """
    変更せず、metadataも更新されないことをチェックする。
    """
    display_name = profile_update_subject.subject.display_name
    email = profile_update_subject.subject.email
    country = profile_update_subject.subject.country
    UpdateSubjectsDomainService.update_profile(profile_update_subject)
    assert profile_update_subject.subject.display_name == display_name
    assert profile_update_subject.subject.email == email
    assert profile_update_subject.subject.country == country
    assert profile_update_subject.metadata.updated_at == profile_update_subject.metadata.created_at


def test_update_profile_invalid_subject(basic_settings_update_subject):
    """
    不正なsubjectを入力した場合にValueErrorが発生することをチェックする。
    """
    with pytest.raises(ValueError):
        UpdateSubjectsDomainService.update_profile(basic_settings_update_subject)


@pytest.mark.parametrize(
        "values",
        [
            {"is_public": False}
        ]
)
def test_update_basic_settings_success(basic_settings_update_subject, values):
    """
    basic_settingsの更新可能であることをチェックする。
    想定通り更新されることをチェックする。
    """
    UpdateSubjectsDomainService.update_basic_settings(basic_settings_update_subject, **values)
    for k, v in values.items():
        if k == "is_public":
            assert basic_settings_update_subject.subject.is_public == v
    assert basic_settings_update_subject.metadata.updated_at != basic_settings_update_subject.metadata.created_at


def test_update_basic_settings_no_change(basic_settings_update_subject):
    is_public = basic_settings_update_subject.subject.is_public
    UpdateSubjectsDomainService.update_basic_settings(basic_settings_update_subject)
    assert basic_settings_update_subject.subject.is_public == is_public
    assert basic_settings_update_subject.metadata.updated_at == basic_settings_update_subject.metadata.created_at


def test_update_basic_settings_invalid_subject_failure(profile_update_subject):
    """
    不正なsubjectを入力した場合にValueErrorが発生することをチェックする。
    """
    with pytest.raises(ValueError):
        UpdateSubjectsDomainService.update_basic_settings(profile_update_subject)