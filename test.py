from enum import Enum


class TEST(Enum):
    TEST="TEST"

print(isinstance(TEST.TEST, TEST))