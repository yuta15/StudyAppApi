import pytest

from src.app.model.shared.validation import validate_value_type


def test_validate_value_type_success_accepts_valid_type():
    """指定した型の値は許可されること。"""

    # Assert
    validate_value_type(value="title", valid_type=str)


@pytest.mark.parametrize(
    ("value", "valid_type"),
    [
        (None, str),
        (1, str),
        ("not-int", int),
    ],
    ids=["none", "integer_for_str", "string_for_int"],
)
def test_validate_value_type_failure_invalid_type(value, valid_type):
    """指定した型ではない値は許可されないこと。"""

    # Assert
    with pytest.raises(ValueError):
        validate_value_type(value=value, valid_type=valid_type)
