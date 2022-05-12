from abc import ABC, abstractmethod
from datetime import date
from typing import List

from packages.entities.candidate import Candidate


class IPersistence(ABC):
    @abstractmethod
    def get_records_by_criteria(self, criteria: str) -> List[dict] | None:
        raise NotImplementedError

    def add_or_update_record(self, record: dict, record_id=None) -> str:
        raise NotImplementedError

    def upload_file(self, record_id, file_path: str) -> str:
        raise NotImplementedError

    def get_records_by_year(self, year: int) -> List[dict]:
        raise NotImplementedError

    def get_record_by_month(self, month: int, year: int) -> dict:
        raise NotImplementedError

    def persist_to_file(self, _date: date, aggregated_info: dict, candidates: List[Candidate]) -> str:
        raise NotImplementedError