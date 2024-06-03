from functools import cached_property
from pathlib import Path
import random
import shutil
import string
import subprocess
import sys
import os

from src.utils import Grade, LabTemplate, Lab

class ExampleLabLabTemplate(LabTemplate):
    # DB properties
    lab_template_id: int = -1
    # Used only when seeding for the first time
    seed_name: str = "Example lab"
    seed_section: str = "Example Chapter"
    seed_short_description: str = (
        "Example description"
    )
    seed_long_description: str = "Example long description "
    seed_active: bool = False
    # Static dir
    static_dir: Path = Path(__file__).parent

    @staticmethod
    def _grade(submitted_solution: str, solution: str) -> Grade:
        """Grades a submissions
        """


        score = 0
        feedback = "example"

        return Grade(score=score, feedback=feedback)

    def generate_lab(self, *, user_id: int = 0, seed: str = "", debug: bool = False) -> Lab:  # type: ignore

        random.seed(seed)

        solution = "Example"

        return Lab(
            lab_template_id=self.lab_template_id,
            user_id=user_id,
            seed=seed,
            unique_question_file=self._zip_temp_lab_dir_and_read(),
            solution=solution,
        )


if __name__ == "__main__":
    ExampleLab().generate_lab()
