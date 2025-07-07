from abc import ABC, abstractmethod

from src.shared.domain.value_objects import Id

from .models import Cv, Education, WorkExperience, Skill


class CvsRepository(ABC):
    @abstractmethod
    def all(self) -> list[Cv]: ...

    @abstractmethod
    def save(self, cv: Cv) -> None: ...

    @abstractmethod
    def exists_by_id(self, id: Id) -> bool: ...

    @abstractmethod
    def get_by_id(self, id: Id) -> Cv: ...


class WorkExperiencesRepository(ABC):
    @abstractmethod
    def all_by_cv_id(self, cv_id: Id) -> list[WorkExperience]: ...

    @abstractmethod
    def save(self, work_experience: WorkExperience) -> None: ...


class EducationsRepository(ABC):
    @abstractmethod
    def all_by_cv_id(self, cv_id: Id) -> list[Education]: ...

    @abstractmethod
    def save(self, education: Education) -> None: ...


class CoursesRepository(ABC):
    @abstractmethod
    def all_by_cv_id(self, cv_id: Id) -> list[Education]: ...

    @abstractmethod
    def save(self, education: Education) -> None: ...


class SkillsRepository(ABC):
    @abstractmethod
    def all_by_cv_id(self, cv_id: Id) -> list[Skill]: ...
    
    @abstractmethod
    def save(self, skill: Skill) -> None: ...