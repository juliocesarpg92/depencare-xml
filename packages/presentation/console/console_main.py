from datetime import date
import calendar

import packages.adapters.file_persistence.zohoCreator.creator as zohoCreator
from packages.adapters.configuration.configuration import Configuration
from packages.adapters.zohoSDK.zoho_api_requests import ApiRequestRepository
from packages.use_cases.annual_info import AnnualInfo
from packages.use_cases.monthly_info import MonthlyInfo

# crear config
config = Configuration()
# crear creator
creator = zohoCreator.Creator(config)


def __menu():
    # recoger info sobre tipo de xml
    xml_type = int(input(
        '''
        Tipo de XML a generar:
        1 - Mensual
        2 - Anual
        0 - Salir\n
        '''
    ))
    return xml_type


def __process_month():
    # recoger info de fechas
    month = int(input('Seleccione un mes del 1 al 12: '))
    year = int(input('Entre un año: '))
    month_last_day = calendar.monthrange(year, month)[1]
    start_date = date(year, month, 1)
    end_date = date(year, month, month_last_day)
    # crear repositorio
    repository = ApiRequestRepository()
    # ejecutar la peticion de info mensual al zoho
    monthly_info = MonthlyInfo(start_date, end_date, repository)()
    candidates, aggregated_info = monthly_info.values()
    # crear xml local
    xml_file_path = creator.persist_to_file(start_date, aggregated_info, candidates)
    # actualizar o agregar el registro en el creator
    record_from_creator = creator.get_record_by_month(month, year)
    record_id = record_from_creator['ID'] if record_from_creator is not None else None
    record_to_save = dict(data=aggregated_info)
    record_id = creator.add_or_update_record(record_to_save, record_id)
    # subir xml al creator
    creator.upload_file(record_id, xml_file_path)


def __process_annual():
    # recoger info de fechas
    year = int(input('Entre un año: '))
    # ejecutar la peticion de info al creator
    annual_info = AnnualInfo(year, creator)()
    # crear xml local
    xml_file_path = creator.persist_to_file(year, annual_info)


def __process(xml_type: int):
    if xml_type == 0:
        pass
    else:
        if xml_type == 1:
            __process_month()
        elif xml_type == 2:
            __process_annual()


def execute():
    try:
        choice = -1
        while choice != 0:
            choice = __menu()
            __process(choice)
    except Exception as e:
        print('Errors occurred')
