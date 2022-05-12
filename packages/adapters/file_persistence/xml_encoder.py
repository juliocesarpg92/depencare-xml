from datetime import date


def xml_encode_object(object_to_encode: dict, father_tag: str, margin=2) -> str:
    start_tag = '<'
    end_tag = '>'
    start_close_tag = '</'
    root_key_margin = '\t' * margin
    inner_keys_margin = '\t' * (margin + 1)
    xml = f"\n{root_key_margin}{start_tag}{father_tag.upper()}{end_tag}"

    for key, value in object_to_encode.items():
        if value is None:
            value = ''
        if key in ['Anho', 'Mes', 'Total_personas_receptores']:
            continue
        encoded_row = f"\n{inner_keys_margin}{start_tag}{key.upper()}{end_tag}{value}{start_close_tag}{key.upper()}{end_tag}"
        xml += encoded_row
    return xml + f"\n{root_key_margin}{start_close_tag}{father_tag.upper()}{end_tag}"


def xml_wrapper(_date: date | int, aggregated_data: str, candidates: str = '') -> str:
    if type(_date) == date:
        isodate = _date.isoformat().replace('-', '')
        year = isodate[:4]
        month = isodate[4:6]
    else:
        year = _date
        month = 99
    return \
        f'''<?xml version="1.0" encoding="ISO-8859-1"?>
<ENVIO_ENPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <ENVIO_MENSUAL>
        <CODIGO_AGENCIA>9900000686</CODIGO_AGENCIA>
        <AÑO_MES_ENVIO>{year}{month}</AÑO_MES_ENVIO>
        <ACCIONES_REALIZADAS>{candidates}
        </ACCIONES_REALIZADAS>{aggregated_data}
    </ENVIO_MENSUAL>
</ENVIO_ENPI>
'''


if __name__ == '__main__':
    print('Testing xml encode object')
    candidates_dict = {'key1': 'value1', 'key2': None}
    candidates = xml_encode_object(candidates_dict, 'accion', 3)
    aggregated_data_dict = {'key1': 10, 'key2': 0}
    aggregated_data = xml_encode_object(aggregated_data_dict, 'datos_agregados')

    print('Testing xml wrapper with month')
    xml = xml_wrapper(date(1962, 2, 17), aggregated_data, candidates)
    print(xml)

    print('Testing xml wrapper without month for annual xml')
    xml = xml_wrapper(1962, aggregated_data)
    print(xml)
