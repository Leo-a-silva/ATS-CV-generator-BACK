from abc import ABC, abstractmethod
from .models import Cv


class CvsRepository(ABC):
    @abstractmethod
    def all(self) -> list[Cv]: ...

    @abstractmethod
    def save(self, cv: Cv) -> None: ...
