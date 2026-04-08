from typing import TypeVar


T = TypeVar("T")


def is_valid_type(value:str, valid_type:type[T]) -> None:
    if not isinstance(value, valid_type):
        raise ValueError(f"タイプが違います. value:{value}, type:{valid_type}")
    return