from datetime import date


def format_date(to_format: date or str):
    if to_format is None:
        raise ValueError("Fecha_inicio_actividad(Servicio Cuidador) o Fecha_de_Nacimiento(Cuidador) están vacías")
    if isinstance(to_format, date):
        to_format = date.isoformat()
    formatted = to_format.replace('-', '')
    return formatted


def format_carer_service(carer_service):
    '''
    formatear fechas y eliminar objetos anidados
    :param carer_service:
    :return: dict
    '''
    carer_service['SC_Cliente_Empleador'] = carer_service['SC_Cliente_Empleador']['id']
    carer_service['Cuidador'] = carer_service['Cuidador']['id']
    carer_service['Fecha_inicio_actividad'] = format_date(carer_service['Fecha_inicio_actividad'])

    tipo_contrato = '000'
    if carer_service['Codigo_tipo_contrato_cuidador'] is not None:
        tipo_contrato = carer_service['Codigo_tipo_contrato_cuidador'].split(':')[0]
        if tipo_contrato == '100':
            tipo_contrato = '001'
        elif tipo_contrato == '200':
            tipo_contrato = '003'
    carer_service['Codigo_tipo_contrato_cuidador'] = tipo_contrato

    return carer_service


def format_carer(carer: dict):
    '''
    formatear fechas y eliminar objetos anidados
    :param carer:
    :return: dict
    '''
    try:
        # carer['Indicador_colectivo_dificultades_insercion'] = 'S' if carer['Indicador_colectivo_dificultades_insercion'] == 'SI' else 'N'

        carer['Indicador_discapacidad'] = 'S' if carer['Indicador_discapacidad'] == 'SI' else 'N'

        # carer['Indicador_recibe_prestaciones_desempleo'] = 'S' if carer['Indicador_recibe_prestaciones_desempleo'] == 'SI' else 'N'

        carer['Indicador_inmigrante'] = 'N' if carer['Indicador_inmigrante'] == 'NO' else 'S'  # TODO: duda en este, pues en caso q sea None sería inmigrante el cuidador

        nivel_formativo = '10'
        if carer['Nivel_formativo'] is not None and carer['Nivel_formativo'].startswith(('00', '10', '20', '30')):
            nivel_formativo = carer['Nivel_formativo'].split('-')[0]
        carer['Nivel_formativo'] = nivel_formativo.strip()

        carer['Sexo'] = '1' if carer['Sexo'] == 'Hombre' else '2'

        # se usa para calcular la edad, usada por el filtro de problemas de inserción
        carer['Fecha_de_Nacimiento_iso_date'] = carer['Fecha_de_Nacimiento']

        carer['Fecha_de_Nacimiento'] = format_date(carer['Fecha_de_Nacimiento'])

        carer['Nombre'] = carer['Nombre'].lower() if carer['Nombre'] else None
        carer['Nombre'] = __format_names(carer['Nombre'])

        carer['Apellidos'] = carer['Apellidos'].lower() if carer['Apellidos'] else None
        carer['Apellidos'] = __format_lastnames(carer['Apellidos'])

        carer['Segundo_apellido_cuidador'] = carer['Segundo_apellido_cuidador'].lower() if carer['Segundo_apellido_cuidador'] else None
        carer['Segundo_apellido_cuidador'] = __format_lastnames(carer['Segundo_apellido_cuidador'])

        if carer['DNI_NIE_Permiso_de_trabajo'] is None:
            raise ValueError('el dni es nulo')
        carer['DNI_NIE_Permiso_de_trabajo'] = carer['DNI_NIE_Permiso_de_trabajo'].replace('-','')
        if len(carer['DNI_NIE_Permiso_de_trabajo']) != 9:
            raise ValueError('el dni debe tener exactamente 9 caracteres')

        return carer
    except Exception as ex:
        print(f'error en cuidador {carer["Nombre"]} {carer["Apellidos"]} {carer["Segundo_apellido_cuidador"]}')
        print(ex)
        raise

# TODO: hacer un mecanismo para garantizar la corrección de los datos 
def format_client(client: dict):
    try:
        client['cif_nif_empresa'] = client['Num_documento_Empleador']
        client['razon_social_empresa'] = ' '.join(
            [
                client.get('Nombre_y_Apellidos_empleador') if client.get('Nombre_y_Apellidos_empleador') != None else '',
                client.get('Apellidos_empleador') if client.get('Apellidos_empleador') != None else '',
                client.get('Segundo_apellido_empleador') if client.get('Segundo_apellido_empleador') != None else ''
            ])
        
        return client
    except Exception as ex:
        print(f'error en cliente {client}')
        print(ex)
        raise

def __format_names(name_to_format):
    if name_to_format is not None:
        name_to_format = name_to_format.rstrip()
        if len(name_to_format) > 15:
            name_to_format = name_to_format[:14]
            name_to_format += '.'
    return name_to_format

def __format_lastnames(lastname_to_format):
    if lastname_to_format is not None:
        lastname_to_format = lastname_to_format.rstrip()
        if len(lastname_to_format) > 20:
            lastname_to_format = lastname_to_format[:19]
            lastname_to_format += '.'
    return lastname_to_format


if __name__ == '__main__':
    # print('Testing date format')
    # date_to_format = date(2021, 8, 1)
    # print(format_date(date_to_format))

    # print('Testing name format')
    # name_to_format = 'elisabeth marciana'
    # # name_to_format = 'elisabethmarcia '
    # # name_to_format = 'None '
    # formatted_name =  __format_names(name_to_format)
    # print(formatted_name)
    # print(len(formatted_name))

    print('Testing lastname format')
    lastname_to_format = 'ramírez patricio de heredia'
    # lastname_to_format = 'elisabethmarcia '
    # lastname_to_format = 'None '
    formatted_lastname = __format_lastnames(lastname_to_format)
    print(formatted_lastname)
    print(len(formatted_lastname))
