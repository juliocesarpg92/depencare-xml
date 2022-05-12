from datetime import date
from typing import List

from zcrmsdk.src.com.zoho.crm.api import ParameterMap
from zcrmsdk.src.com.zoho.crm.api.query import BodyWrapper, APIException, ResponseWrapper
from zcrmsdk.src.com.zoho.crm.api.query import QueryOperations
from zcrmsdk.src.com.zoho.crm.api.record import Record, RecordOperations, GetRecordsParam

from packages.adapters.utils.format_for_entities import format_carer_service, format_carer, format_client
from packages.adapters.zohoSDK.auth.sdk_initializer import initialize
from packages.entities.interfaces.interface_repository import IRepository


def _fetch_from_api_with_sql(module_name: str, select_fields: str, where_clause: str) -> List[dict]:
    records_from_api: List[Record] = []
    more_records_from_api = True
    # Get instance of QueryOperations Class
    query_operations = QueryOperations()
    # Get instance of BodyWrapper Class that will contain the request body
    body_wrapper = BodyWrapper()
    page = 1
    limit = 200

    while more_records_from_api:
        offset = limit * (page - 1)
        # TODO: ninguno de los valores que devuelve (fields) puede ser null o '' (revisar función existeError)
        select_query = "select {fields} from {module} " \
                       "where {where_clause} " \
                       "limit {offset}, {limit}".format(fields=select_fields, module=module_name,
                                                        where_clause=where_clause,
                                                        limit=limit, offset=offset)
        body_wrapper.set_select_query(select_query)
        try:
            # Call get_records method that takes BodyWrapper instance as parameter
            api_response = query_operations.get_records(body_wrapper).get_object()
            if isinstance(api_response, ResponseWrapper):
                records_from_api.extend(api_response.get_data())
                more_records_from_api = api_response.get_info().get_more_records()
                page += 1
            if isinstance(api_response, APIException):
                more_records_from_api = False
                raise Exception('error in module ' + module_name + '\n' + api_response.get_message().get_value())
            if api_response is None:
                more_records_from_api = False
                if page == 1:
                    print(f'No records from {module_name}')
        except Exception as e:
            print(e)
            raise

    iterator = map(lambda record: record.get_key_values(), records_from_api)
    return list(iterator)


def _fetch_from_api_with_ids(module_name: str, record_ids: List[int or str] or int or str, fields: List[str] = None) -> \
        List[dict]:
    # Get instance of RecordOperations Class
    record_operations = RecordOperations()
    # Get instance of ParameterMap Class
    param_instance = ParameterMap()
    if isinstance(record_ids, List):
        for each_id in record_ids:
            param_instance.add(GetRecordsParam.ids, int(each_id))
    else:
        param_instance.add(GetRecordsParam.ids, int(record_ids))
    # param_instance.add(GetRecordsParam.uid, '3409643000000302031')
    if fields is not None:
        for field in fields:
            param_instance.add(GetRecordsParam.fields, field)
    # Call getRecords method that takes ParameterMap Instance and module_api_name as parameters
    response = record_operations.get_records(module_name, param_instance)

    iterator = map(lambda record: record.get_key_values(), response.get_object().get_data())
    return list(iterator)


class ApiRequestRepository(IRepository):
    """
    Peticiones de datos al API de Zoho
    """

    def __init__(self):
        initialize()

    def get_new_candidates(self, start_date: date, end_date: date) -> list[dict]:
        """
        Recoger nuevos candidatos
        :return: List[dict]
        """
        # TODO: hacer logging
        select_fields = 'Nombre,Apellidos,Segundo_apellido_cuidador,Fecha_de_Nacimiento,DNI_NIE_Permiso_de_trabajo,' \
                        'Indicador_recibe_prestaciones_desempleo,Indicador_discapacidad,Indicador_inmigrante,' \
                        'Indicador_colectivo_dificultades_insercion,Nivel_formativo,Sexo,Fecha_de_aceptacion'
        where_clause = "Fecha_de_aceptacion between \'{start}\' and \'{end}\' ".format(start=start_date, end=end_date)
        module = 'Cuidadores'
        new_candidates: List[dict] = _fetch_from_api_with_sql(module, select_fields, where_clause)
        new_candidates = list(map(format_carer, new_candidates))
        return new_candidates

    def get_deals_n_offers(self, start_date: date, end_date: date) -> List[dict]:
        """
        Recoger número de puestos y ofertas
        :return: List[dict]
        """
        # TODO: hacer logging
        select_fields = 'Numero_de_cuidadores'
        where_clause = "Fecha_inicio_busqueda between \'{start}\' and \'{end}\' " \
                       "and Stage in (\'SLD Ppto aceptado\',\'SLD Preparación\',\'SLD Busqueda\',\'SLD con Cuidador\',\'SLD Vivo\',\'SLD Finalizado\',\'SLD Cancelado\')".format(
            start=start_date, end=end_date)
        module = 'Deals'
        deals: List[dict] = _fetch_from_api_with_sql(module, select_fields, where_clause)
        return deals

    def get_carer_services(self, start_date: date, end_date: date) -> list[dict]:
        """
        Recoger servicios cuidador
        :return: List[dict]
        """
        # TODO: hacer logging
        select_fields = 'SC_Cliente_Empleador, Name, Codigo_tipo_contrato_cuidador, Cuidador, Fecha_inicio_actividad'
        where_clause = "Fecha_inicio_actividad between \'{start}\' and \'{end}\' " \
                       "and Estado in (\'SCLD Tramitado\',\'SCLD Prebaja\',\'SCLD Baja definitiva\',\'SCLD Finalizado\',\'SC Fin con feedback\')".format(
            start=start_date, end=end_date)
        module = 'Historico_de_cuidadores'
        carer_services: List[dict] = _fetch_from_api_with_sql(module, select_fields, where_clause)
        carer_services = list(map(format_carer_service, carer_services))
        return carer_services

    def get_client_by_id(self, client_id) -> dict:
        """
        Devolver cliente dado el id
        :return: List[dict]
        """
        # TODO: hacer logging
        select_fields = 'Num_documento_Empleador,' \
                        'Nombre_y_Apellidos_empleador,' \
                        'Apellidos_empleador,Segundo_apellido_empleador'
        where_clause = 'id = {id}'.format(id=client_id)
        module = 'Contacts'
        client: dict = _fetch_from_api_with_sql(module, select_fields, where_clause)[0]
        client = format_client(client)
        return client

    def get_carer_by_id(self, carer_id) -> dict:
        """
        Devolver cuidador dado el id
        :return: List[dict]
        """
        # TODO: hacer logging
        select_fields = 'Nombre,Apellidos,Segundo_apellido_cuidador,Fecha_de_Nacimiento,DNI_NIE_Permiso_de_trabajo,' \
                        'Indicador_recibe_prestaciones_desempleo,Indicador_discapacidad,Indicador_inmigrante,' \
                        'Indicador_colectivo_dificultades_insercion,Nivel_formativo,Sexo'
        where_clause = 'id = {id}'.format(id=carer_id)
        module = 'Cuidadores'
        carer: dict = _fetch_from_api_with_sql(module, select_fields, where_clause)[0]
        carer = format_carer(carer)
        return carer

    def get_interviews(self, start_date: date, end_date: date) -> list[dict]:
        """
        Recoger entrevistas
        :return: List[dict]
        """
        # TODO: hacer logging
        select_fields = 'SC_Cliente_Empleador, Name, Codigo_tipo_contrato_cuidador, Cuidador'
        where_clause = "Fecha_envio_datos between \'{start}\' and \'{end}\' " \
                       "and Estado in (\'SCLD Tramitado\',\'SCLD Prebaja\',\'SCLD Baja definitiva\',\'SCLD Finalizado\',\'SC Fin con feedback\',\'SCLD Bloqueado\',\'SCLD Asignado\',\'SCLD Rechazado\')".format(
            start=start_date, end=end_date)
        module = 'Historico_de_cuidadores'
        carer_services: List[dict] = _fetch_from_api_with_sql(module, select_fields, where_clause)
        return carer_services


if __name__ == "__main__":
    print("Running Zoho Api Requests Tests")
    api_request = ApiRequestRepository()

    # print("Testing Get Objects with ids")
    # # ZCRM_SCUI967,ZCRM_SCUI966
    # ids = [80617000008245202, 80617000001250015]
    # # ids = 80617000008245202
    # response = api_request._fetch_from_api_with_ids('Cuidadores', ids)
    # record_list: List[Record] = response
    # print('listado de cuidadores por id')
    # for record in record_list:
    #     print(record.get_key_values()['Name'])

    # print("Testing get client by id")
    # id = '80617000011515391'
    # client = api_request.get_client_by_id(id)
    # print(client)

    # print("Testing get carer by id")
    # id = '80617000008245202'
    # carer = api_request.get_carer_by_id(id)
    # print(carer)

    # print("Testing New Candidates")
    # start = date(2021, 12, 1)
    # end = date(2021, 12, 31)
    # response = api_request.get_new_candidates(start, end)
    # record_list: List[Record] = response
    # print('listado de cuidadores')
    # for record in record_list:
    #     print(record['Nombre'], record['Fecha_de_aceptacion'])

    # print("Testing Deals")
    # start = date(2021, 8, 1)
    # end = date(2021, 8, 31)
    # response = api_request.get_deals_n_offers(start, end)
    # record_list: List[dict] = response
    # print('listado de ofertas')
    # print(record_list)

    # print("Testing carer services")
    # start = date(2021, 8, 1)
    # end = date(2021, 8, 31)
    # response = api_request.get_carer_services(start, end)
    # record_list: List[dict] = response
    # print('listado de candidatos con colocación')
    # print(record_list)
    # for record in record_list:
    #     # obtener id del empleador y del cuidador
    #     # print(record.get_key_values().get('SC_Cliente_Empleador')['id'])
    #     # print(record.get_key_values().get('Cuidador')['id'])
    #
    #     # obtener el código del tipo de contrato
    #     # if str(record.get_key_value('Codigo_tipo_contrato_cuidador')).startswith(('401','100','501','200')):
    #         print(record.get_key_values())
