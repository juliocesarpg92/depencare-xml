from typing import List

from packages.entities.aggregated_info import AggregatedInfo
from packages.entities.interfaces.interface_persistence import IPersistence


class AnnualInfo(AggregatedInfo):
    """
    Caso de uso - devolver información anual
    """

    def __init__(self, year: int, from_persistence: IPersistence, start_month: int = 1):
        super().__init__()
        self.__from_persistence = from_persistence
        self.__start_month = start_month
        self.__year = year

    def __summarize(self, records: List) -> dict:
        response = self.to_dict()
        keys = response.keys()
        for record in records:
            for key in keys:
                if key == 'Total_personas_perceptores':
                    response['Total_personas_perceptores'] += int(record['Total_personas_receptores'])
                else:
                    response[key] += int(record[key])
        return response

    def __call__(self) -> dict:
        print('get records from persistence')
        annual_records = self.__from_persistence.get_records_by_year(self.__year)
        print('summarize')
        summarized = self.__summarize(annual_records)
        return summarized


if __name__ == '__main__':
    from packages.adapters.file_persistence.zohoCreator.creator import Creator, CreatorConfig

    creator_config = CreatorConfig()
    creator = Creator(creator_config)
    year = 2021
    info = AnnualInfo(year, creator)

    print('Test summarize method')
    test_list = [
        {
            'total_personas': 10,
            'total_nuevas_registradas': 10,
            'total_personas_perceptores': 10,
            'total_personas_insercion': 10,
            'total_ofertas': 10,
            'total_ofertas_enviadas': 10,
            'total_ofertas_cubiertas': 10,
            'total_puestos': 10,
            'total_puestos_cubiertos': 10,
            'total_contratos': 10,
            'total_contratos_indefinidos': 10,
            'total_personas_colocadas': 10
        },
        {
            'total_personas': 5,
            'total_nuevas_registradas': 5,
            'total_personas_perceptores': 5,
            'total_personas_insercion': 5,
            'total_ofertas': 5,
            'total_ofertas_enviadas': 5,
            'total_ofertas_cubiertas': 5,
            'total_puestos': 5,
            'total_puestos_cubiertos': 5,
            'total_contratos': 5,
            'total_contratos_indefinidos': 5,
            'total_personas_colocadas': 5
        }
    ]
    # print(info._AnnualInfo__summarize(test_list))

    print('Test annual info')
    annualInfoResponse = info()
    print(annualInfoResponse)
