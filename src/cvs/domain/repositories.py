from abc import ABC, abstractmethod

from src.shared.domain.value_objects import Id

from .models import Cv, WorkExperience


class CvsRepository(ABC):
    @abstractmethod
    def all(self) -> list[Cv]: ...

    @abstractmethod
    def save(self, cv: Cv) -> None: ...


class WorkExperiencesRepository(ABC):
    @abstractmethod
    def all_by_cv_id(self, cv_id: Id) -> list[WorkExperience]: ...

    @abstractmethod
    def save(self, work_experience: WorkExperience) -> None: ...
