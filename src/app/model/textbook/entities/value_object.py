from dataclasses import dataclass
from enum import Enum

from src.app.model.shared.validation import validate_value_type


class TextbookStatus(Enum):
    """教材本体のワークフロー状態を表す。"""

    DRAFT = "DRAFT"
    IN_REVIEW = "IN_REVIEW"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


@dataclass(frozen=True)
class TitleString:
    """教材ドメインで利用するタイトル文字列を表す。"""

    value: str

    def __post_init__(self) -> None:
        validate_value_type(value=self.value, valid_type=str)
        if self.value == "" or self.value != self.value.strip():
            raise ValueError("title must not be blank or contain surrounding whitespace")
