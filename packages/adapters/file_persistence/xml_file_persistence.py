import calendar
import os
from datetime import date
from os import getcwd, path, mkdir
from typing import List

from packages.adapters.zohoSDK.zoho_api_requests import ApiRequestRepository
from packages.use_cases.annual_info import AnnualInfo
from packages.use_cases.monthly_info import MonthlyInfo
from .xml_encoder import xml_encode_object, xml_wrapper
from packages.entities.candidate import Candidate


def _get_month_name(index):
    months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
              'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    return months[index]


class XMLPersistence():
    def __init__(self, xml_path: str):
        self.__path = xml_path

    def persist_monthly_info(self, _date: date, aggregated_info: dict, candidates: List[Candidate]) -> str:
        month = _get_month_name(_date.month - 1)
        filename = path.join(self.__path, f"Mensual-{month}{_date.year}-DC.xml")
        if not path.exists(self.__path):
            mkdir(self.__path)

        content_aggregated = xml_encode_object(aggregated_info, 'datos_agregados')
        content_candidates = ''
        for candidate in candidates:
            content_candidates += xml_encode_object(candidate.to_dict(), 'accion', 3)

        with open(filename, 'w', encoding='ISO-8859-1') as writer:
            xml_content = xml_wrapper(_date, content_aggregated, content_candidates)
            writer.write(xml_content)
        return filename

    def persist_annual_info(self, year: int, aggregated_info: dict) -> str:
        filename = path.join(self.__path, f"Anual-{year}-DC.xml")
        if not path.exists(self.__path):
            mkdir(self.__path)

        content_aggregated = xml_encode_object(aggregated_info, 'datos_agregados')

        with open(filename, 'w', encoding='ISO-8859-1') as writer:
            xml_content = xml_wrapper(year, content_aggregated)
            writer.write(xml_content)
        return filename


if __name__ == '__main__':
    repo = ApiRequestRepository()
    year = 2022
    month = 1
    month_last_day = calendar.monthrange(year, month)[1]
    start = date(year, month, 1)
    end = date(year, month, month_last_day)
    info = MonthlyInfo(start, end, repo)
    candidates, aggregated_info = info().values()

    print('Testing monthly xml content before write')
    xmlPersistence = XMLPersistence()
    monthly_path = xmlPersistence.persist_monthly_info(start, aggregated_info, candidates)
    print(monthly_path)

    # print('Testing annual xml content before write')
    # from .zohoCreator.creator import Creator, CreatorConfig
    # year = 2021
    # creator_config = CreatorConfig()
    # creator = Creator(creator_config)
    # info = AnnualInfo(year, creator)
    # aggregated_info = info()
    # annual_path = xmlPersistence.persist_annual_info(year, aggregated_info)
    # print(annual_path)
