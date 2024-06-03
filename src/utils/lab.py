from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Lab:
    user_id: int
    lab_template_id: int
    seed: str
    unique_question_file: bytes
    solution: str
    creation_time: datetime = datetime.now()
    lab_id: int = 0
