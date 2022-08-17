from ciftools.cif_format.base import CIFColumnBase
from ciftools.cif_format.value_presence import ValuePresenceEnum


class UndefinedCIFColumn(CIFColumnBase):
    def is_defined(self) -> bool:
        return False

    def get_string(self, row: int) -> str:
        return ""

    def get_integer(self, row: int) -> int:
        return 0

    def get_float(self, row: int) -> float:
        return 0.0

    def get_value_presence(self, row: int) -> ValuePresenceEnum:
        return ValuePresenceEnum.NotSpecified

    def are_values_equal(self, row_a: int, row_b: int) -> bool:
        return True

    def string_equals(self, row: int, value: str) -> bool:
        return value == ""
