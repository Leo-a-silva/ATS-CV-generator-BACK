from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Id:
    value: int

    def __post_init__(self) -> None:
        if self.value is None:
            raise ValueError("Id cannot be None")
        if not isinstance(self.value, int):
            raise ValueError("Id must be an integer")
        if self.value <= 0:
            raise ValueError("Id must be positive")

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other) -> bool:
        if isinstance(other, Id):
            return self.value == other.value
        return False

    def __hash__(self) -> int:
        return hash(self.value)
