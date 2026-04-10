from typing import TypeVar, Any


T = TypeVar("T")


def validate_value_type(value:Any, valid_type:type[T]) -> None:
    if not isinstance(value, valid_type):
        raise ValueError(f"タイプが違います. value:{value}, type:{valid_type}")
    return