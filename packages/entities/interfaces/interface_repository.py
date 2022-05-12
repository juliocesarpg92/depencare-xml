from abc import abstractmethod, ABC
from datetime import date
from typing import List


class IRepository(ABC):
    @abstractmethod
    def get_new_candidates(self, start_date: date, end_date: date) -> List[dict]:
        raise NotImplementedError

    @abstractmethod
    def get_deals_n_offers(self, start_date: date, end_date: date) -> List[dict]:
        raise NotImplementedError

    @abstractmethod
    def get_carer_services(self, start_date: date, end_date: date) -> List[dict]:
        raise NotImplementedError

    @abstractmethod
    def get_client_by_id(self, client_id) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_carer_by_id(self, carer_id) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_interviews(self, start_date: date, end_date: date) -> List[dict]:
        raise NotImplementedError
