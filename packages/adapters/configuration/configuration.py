import sys
from configparser import ConfigParser, ExtendedInterpolation
from os import path

from requests import post, HTTPError

"""
Información sobre generar los códigos de acceso
https://www.zoho.com/creator/help/api/v2/authorization-request.html

Scopes utilizados
ZohoCreator.report.READ,
ZohoCreator.form.CREATE,
ZohoCreator.report.UPDATE,
ZohoCreator.report.CREATE
"""


class Configuration:

    def __init__(self):
        self.__config_parser = ConfigParser(interpolation=ExtendedInterpolation())
        self.read_config_file()
        # if self.__config_parser['sdk']['token_persistence_path'] == '':
        self.__config_parser['sdk']['token_persistence_path'] = path.join(path.dirname(
                self.__config_file_path), 'sdk/python_sdk_tokens.txt')
        # if self.__config_parser['sdk']['log_file_path'] == '':
        self.__config_parser['sdk']['log_file_path'] = path.join(path.dirname(
                self.__config_file_path), 'sdk/logs/python_sdk_log.log')
        # if self.__config_parser['sdk']['resource_path'] == '':
        self.__config_parser['sdk']['resource_path'] = path.join(path.dirname(
                self.__config_file_path), 'sdk')
        self.__config_parser['sdk']['xml_path'] = path.join(path.dirname(
            self.__config_file_path), 'XMLs')
        self.__write_config_file()

    def get(self, section: str, item: str):
        return self.__config_parser[section][item]

    def __set_creator_access_token(self, new_access_token: str):
        self.__config_parser['creator']['access_token'] = new_access_token
        self.__write_config_file()

    def __write_config_file(self):
        file_opened = open(self.__config_file_path, 'w')
        self.__config_parser.write(file_opened)

    def read_config_file(self):
        config_file_name = 'config.ini'
        if getattr(sys, 'frozen', False):
            self.__config_file_path = path.join(path.dirname(sys.executable), config_file_name)
        else:
            self.__config_file_path = path.join(path.dirname(__file__), config_file_name)
        if not path.exists(self.__config_file_path):
            raise FileNotFoundError("""falta el archivo de configuración,
                                por favor lea el readme
                                """)
        self.__config_parser.read(self.__config_file_path)

    def set_upload_file_url(self, record_id: str) -> str:
        return f'{self.__config_parser["creator"]["report_url"]}/{record_id}/Archivo/upload'

    def get_auth_header(self) -> dict:
        return {'Authorization': 'Zoho-oauthtoken ' + self.__config_parser['creator']['access_token']}

    def was_creator_access_token_invalid(self, http_response: dict):
        # Authorization Failure. The access token is either invalid or has expired
        if http_response['code'] == 1030:
            print('creator access token expired, trying to refresh it')
            if self.__refresh_creator_access_token():
                return True
        return False

    def __refresh_creator_access_token(self) -> bool:
        access_token_response = post(self.__config_parser['creator']['refresh_url'])
        try:
            access_token_response.raise_for_status()
            self.__set_creator_access_token(access_token_response.json()['access_token'])
            print('creator access token refreshed')
            return True
        except HTTPError as http_error:
            print(http_error)
            return False
        except KeyError as key_error:
            print('An error ocurred trying to refresh creator access token')
            print(key_error.__class__, key_error)
            return False


if __name__ == '__main__':
    testConfig = Configuration()

    print(testConfig.get('creator', 'report_link_name'))
    print(testConfig.get('creator', 'refresh_url'))
    print(testConfig.get('creator', 'report_url'))
    print(testConfig.get('creator', 'form_url'))
    print(testConfig.set_upload_file_url('1'))
    print(testConfig.get('sdk', 'token_persistence_path'))
    print(testConfig.get('sdk', 'log_file_path'))
    print(testConfig.get('sdk', 'resource_path'))
