"""
Información sobre generar los códigos de acceso
https://www.zoho.com/creator/help/api/v2/authorization-request.html

Scopes utilizados
ZohoCreator.report.READ,
ZohoCreator.form.CREATE,
ZohoCreator.report.UPDATE,
ZohoCreator.report.CREATE
"""
from datetime import date

from requests import get, ConnectionError, post, HTTPError, patch

from packages.adapters.configuration.configuration import Configuration
from packages.entities.candidate import Candidate
from typing import List
from packages.entities.interfaces.interface_persistence import IPersistence
from packages.adapters.file_persistence.xml_file_persistence import XMLPersistence


class Creator(IPersistence):
    def __init__(self, config: Configuration):
        self.__config = config

    def get_records_by_criteria(self, criteria: str) -> List[dict] | None:
        headers = self.__config.get_auth_header()
        formatted_criteria = 'criteria=' + criteria
        try:
            record_response = get(self.__config.get('creator', 'report_url'), params=formatted_criteria,
                                  headers=headers)
            # No records found for the given criteria
            if record_response.status_code == 404 and record_response.json()['code'] == 3100:
                return None
            # Authorization Failure. The access token is either invalid or has expired
            elif self.__config.was_creator_access_token_invalid(record_response.json()):
                return self.get_records_by_criteria(criteria)
            return record_response.json()['data']
        except ConnectionError as e:
            print('please check internet connection')
        except KeyError as key_error:
            print('An error ocurred trying to get record')
            print(key_error.__class__, key_error)

    def add_or_update_record(self, record: dict, record_id=None) -> str:
        auth_header = self.__config.get_auth_header()
        if record_id is None:
            record_response = post(self.__config.get('creator', 'form_url'), json=record, headers=auth_header)
        else:
            update_url = self.__config.get('creator', 'report_url') + f'/{record_id}'
            record_response = patch(update_url, json=record, headers=auth_header)
        record_response.raise_for_status()
        record_response = record_response.json()
        if record_response['code'] != 3000:
            print(f'Error creating or updating record month {record["Mes"]} year {record["Anho"]}')
            raise Exception(record_response['code'], record_response['description'])
        print(record_response['message'])
        return record_response['data']['ID']

    def get_records_by_year(self, year: int) -> List[dict]:
        criteria = f'Anho={year}'
        response = self.get_records_by_criteria(criteria)
        if response is None or len(response) < 12:
            if response is not None and len(response) < 12:
                months_done = [el['Mes'] for el in response]
                print(months_done)
            raise Exception('some months are missing')
        return response

    def get_record_by_month(self, month: int, year: int) -> dict | None:
        criteria = f'Anho={year}&&Mes={month}'
        response = self.get_records_by_criteria(criteria)
        if response is None:
            return None
        return response[0]

    def upload_file(self, record_id, file_path: str) -> str:
        upload_url = self.__config.set_upload_file_url(record_id)
        auth_header = self.__config.get_auth_header()
        binary_file = {'file': open(file_path, 'rb')}
        file_upload_response = post(upload_url, files=binary_file, headers=auth_header)
        file_upload_response = file_upload_response.json()
        if file_upload_response['code'] != 3000:
            print('error uploading file')
            raise Exception(file_upload_response['code'], file_upload_response['description'])
        print(file_upload_response['data']['message'])
        return file_upload_response['data']['message']

    def persist_to_file(self, _date: date | int, aggregated_info: dict, candidates: List[Candidate] = None) -> str:
        persistence = XMLPersistence(self.__config.get('sdk', 'xml_path'))
        if type(_date) == date:
            path = persistence.persist_monthly_info(_date, aggregated_info, candidates)
        else:
            path = persistence.persist_annual_info(_date, aggregated_info)
        return path


if __name__ == '__main__':
    testConfig = Configuration()
    testCreator = Creator(testConfig)

    searchCriteria = 'Anho=2021&&Mes=4'
    test_record_response = testCreator.get_records_by_criteria(searchCriteria)

    print('get record response', end='--')
    # print(len(response.json()['data']))
    print(test_record_response)

    print('add record')
    record = {
        "data": {
            "Anho": 2023,
            "Mes": 1
        }
    }
    created_id = testCreator.add_or_update_record(record)
    print('Id created -- ' + created_id)

    print('update record')
    record['data']['Total_personas'] = 7357  # 7-t 3-e 5-s
    updated_id = testCreator.add_or_update_record(record, created_id)
    print('Id updated -- ' + updated_id)

    print('upload file to record')
    file_path = '../../configuration/XMLs/Mensual-Enero2022-DC.xml'
    upload_file_response = testCreator.upload_file(created_id, file_path)
    print(upload_file_response)
