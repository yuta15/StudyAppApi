from typing import TypeVar


T = TypeVar("T")


def validate_value_type(value: object, valid_type: type[T]) -> None:
    """値が指定した型であることを検証する。"""

    if not isinstance(value, valid_type):
        raise ValueError(f"タイプが違います. value:{value}, type:{valid_type}")
