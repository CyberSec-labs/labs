from abc import abstractmethod, ABC
from functools import cached_property
from pathlib import Path
import shutil
import os
from fastapi import UploadFile

from .grade import Grade
from .lab import Lab


class LabTemplate(ABC):
    subclasses: dict[int, type["LabTemplate"]] = dict()

    def __init_subclass__(cls, *args, **kwargs):
        """This method essentially creates a list of all subclasses"""

        super().__init_subclass__(*args, **kwargs)
        pre_existing_cls = cls.subclasses.get(cls.lab_template_id)  # type: ignore
        msg = f"Not unique {pre_existing_cls} {cls}"
        assert not pre_existing_cls or pre_existing_cls.__name__ == cls.__name__, msg
        cls.subclasses[cls.lab_template_id] = cls  # type: ignore

    def __init__(
        self, generated_dir: Path = Path.home() / "Desktop" / "generated_labs"
    ):
        self.generated_dir: Path = generated_dir

    def _zip_temp_lab_dir_and_read(self) -> bytes:
        """Zips the generated_dir and reads it as bytes for db insertion"""

        # https://stackoverflow.com/a/25650295/8903959
        shutil.make_archive(str(self.zipped_lab_path), "zip", str(self.temp_lab_dir))
        # For some reason this is .zip.zip due to shutil
        # Could be fixed, but it's also fine
        with Path(str(self.zipped_lab_path) + ".zip").open("rb") as f:
            return f.read()

    def _copy_q_dir_into_lab_generated_dir(self):
        """Copies the question directory into the lab temporary directory"""
        if(os.path.exists(self.temp_lab_dir / "question")):
            shutil.rmtree(self.temp_lab_dir / "question")
        shutil.copytree(self.question_dir, self.temp_lab_dir / "question")

    ###################
    # Path Properties #
    ###################

    @cached_property
    def question_dir(self) -> Path:
        return self.static_dir / "question"

    # I don't think this should ever be used, but just in case I'm leaving it here
    # @cached_property
    # def solution_dir(self) -> Path:
    #     return self.static_dir / "solution"

    @cached_property
    def temp_lab_dir(self) -> Path:
        # Can't use name for folder since it could contain spaces and special chars
        temp_lab_dir = self.generated_dir / "lab"  # self.data["name"]
        temp_lab_dir.mkdir(exist_ok=True, parents=True)
        assert isinstance(temp_lab_dir, Path), "Mypy is erroring here"
        return temp_lab_dir

    @cached_property
    def zipped_lab_path(self) -> Path:
        # Can't use lab name here due to spaces and special chars
        path = self.generated_dir / "lab.zip"  # f'{self.data["name"]}.zip'
        assert isinstance(path, Path), "Mypy is erroring here"
        return path

    ####################
    # Abstract Methods #
    ####################

    @classmethod
    def grade(
        cls: type["LabTemplate"],
        submitted_solution: str,
        solution: str,
        files: UploadFile,
    ) -> Grade:
        """Grades a submissions"""
        try:
            return cls._grade(submitted_solution, solution, files)
        except Exception as e:
            print(e)
            return Grade(score=0, feedback="Error when grading assignment")

    @staticmethod
    @abstractmethod
    def _grade(submitted_solution: str, solution: str) -> Grade:
        """Grades a submissions"""

        raise NotImplementedError

    @property
    @abstractmethod
    def static_dir(self) -> Path:
        """Return static directory containing question and solution files

        Must have in the subclass due to the __file__ always pointing to this class
        """

        # Don't cover abstract methods
        return Path(__file__).parent  # pragma: no cover

    @abstractmethod
    def generate_lab(
        self,
        *,
        user_id: int = 0,
        # This will be constant every time
        # but in the backend we override this for randomness
        seed: str = "0",
    ) -> Lab:
        raise NotImplementedError

    #################
    # DB properties #
    #################

    @property
    @abstractmethod
    def lab_template_id(self) -> int:
        """lab_template_id found in the database"""
        raise NotImplementedError

    @property
    @abstractmethod
    def seed_name(self) -> str:
        """Name to insert into db if not already seeded"""
        raise NotImplementedError

    @property
    @abstractmethod
    def seed_section(self) -> str:
        """Section to insert into db if not already seeded"""
        raise NotImplementedError

    @property
    @abstractmethod
    def seed_short_description(self) -> str:
        """Short desc to insert into db if not already seeded"""
        raise NotImplementedError

    @property
    @abstractmethod
    def seed_long_description(self) -> str:
        """Long desc to insert into db if not already seeded"""
        raise NotImplementedError

    @property
    @abstractmethod
    def seed_active(self) -> bool:
        """active field to insert into db if not already seeded"""
        raise NotImplementedError
