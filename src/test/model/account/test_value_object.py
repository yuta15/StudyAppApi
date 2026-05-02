import string
import pytest

from src.app.model.account import AccountNameStrings, EmailStrings


invalid_char_names = []
for char in list(string.punctuation) + [" ", "\n", "\r"]:
    if char not in ["-", "_"]:
        invalid_char_names.append(f"value_{char}")


@pytest.mark.parametrize(
    "account_name_str",
    [
        pytest.param("1234"),
        pytest.param("test_account_name"),
        pytest.param("test-account-name"),
        pytest.param("test-account_name"),
        pytest.param("1234567890123456789012345"),
    ],
)
def test_account_name_success(account_name_str):
    assert isinstance(AccountNameStrings(value=account_name_str), AccountNameStrings)


@pytest.mark.parametrize("invalid_char_name", invalid_char_names)
def test_account_name_invalid_char_failure(invalid_char_name):
    with pytest.raises(Exception):
        AccountNameStrings(value=invalid_char_name)


@pytest.mark.parametrize("invalid_len_name", ["a" * 3, "a" * 26])
def test_account_name_failure(invalid_len_name):
    with pytest.raises(Exception):
        AccountNameStrings(value=invalid_len_name)


@pytest.mark.parametrize("success_email_str", ["test@example.com", "a@b"])
def test_email_str_success(success_email_str):
    assert isinstance(EmailStrings(success_email_str), EmailStrings)


@pytest.mark.parametrize("failure_email_str", ["testexample.com"])
def test_email_str_failure(failure_email_str):
    with pytest.raises(Exception):
        EmailStrings(failure_email_str)
