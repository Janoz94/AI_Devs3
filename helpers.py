from typing import Union, List
from dataclasses import dataclass


@dataclass
class PayloadBody:
    api_key: str
    task_name: str
    answer: Union[str, List[str], dict]

    def to_dict(self) -> dict:
        return {"task": self.task_name, "apikey": self.api_key, "answer": self.answer}
