from ..domain.repositories import CvsRepository
from ..domain.models import Cv


class SQLModelCvsRepository(CvsRepository):
    def all(self) -> list[Cv]:
        pass

    def save(self, cv: Cv) -> None:
        pass
