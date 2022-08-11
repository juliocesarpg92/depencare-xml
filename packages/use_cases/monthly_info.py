from datetime import date
from typing import List

from packages.entities.aggregated_info import AggregatedInfo
from packages.entities.candidate import Candidate
from packages.entities.interfaces.interface_repository import IRepository


class MonthlyInfo(AggregatedInfo):
    """
    Caso de uso - devolver información mensual
    """

    def __init__(self, start: date, end: date, repository: IRepository):
        super().__init__()
        self.__repository = repository
        self.__start_date = start
        self.__end_date = end
        self.__candidates: List[Candidate] = []
        self.__candidates_no_duplicates: List[str] = []

    def __new_candidates(self) -> None:
        new_candidates = self.__repository.get_new_candidates(self.__start_date, self.__end_date)
        self.total_nuevas_registradas = len(new_candidates)
        for dict_candidate in new_candidates:
            self.__candidates.append(Candidate(dict_candidate))

    def __deals_n_offers(self) -> None:
        deals = self.__repository.get_deals_n_offers(self.__start_date, self.__end_date)
        self.total_ofertas = len(deals)
        for deal in deals:
            if deal['Numero_de_cuidadores'] == '1' or deal['Numero_de_cuidadores'] is None:
                self.total_puestos += 1
            else:
                self.total_puestos += 2

    def __candidates_with_colocation(self) -> None:
        carer_services = self.__repository.get_carer_services(self.__start_date, self.__end_date)
        self.total_ofertas_cubiertas = len(carer_services)
        self.total_puestos_cubiertos = len(carer_services)
        candidates_colocated: List[Candidate] = []
        for service in carer_services:
            client = self.__repository.get_client_by_id(service['SC_Cliente_Empleador'])
            carer = self.__repository.get_carer_by_id(service['Cuidador'])
            candidate = Candidate({**client, **carer, **service})
            candidates_colocated.append(candidate)
        self.__candidates.extend(candidates_colocated)
        # eliminar duplicados de cuidadores colocados en mas de 1 servicio
        candidates_colocated_no_duplicates = {candidate.id_trabajador for candidate in candidates_colocated}
        self.total_personas_colocadas = len(candidates_colocated_no_duplicates)

    def __total_people_count(self):
        people_set = {x.id_trabajador for x in self.__candidates}
        self.total_personas = len(people_set)

    def __summarize(self) -> None:
        self.__total_people_count()

        # guarda los id de los candidatos que ya han sido visitados para garantizar la singularidad de la info donde se necesite
        visited_candidates: List[str] = []

        for candidate in self.__candidates:

            if candidate.colocacion == 'S' and candidate.tipo_contrato != '000':
                self.total_contratos += 1
                if candidate.tipo_contrato in ('001', '003'):
                    self.total_contratos_indefinidos += 1

            if candidate.recibe_prestaciones_desempleo == 'S':
                self.total_personas_perceptores += 1

            birth_date = date.fromisoformat(candidate.fecha_nacimiento_iso_date)
            actual_date = self.__end_date
            years = actual_date.year - birth_date.year
            if candidate.id_trabajador not in visited_candidates:
                if candidate.discapacidad == 'S' \
                        or candidate.dificultades_insercion in ('SI', '') \
                        or candidate.sexo_trabajador != 1 \
                        or candidate.inmigrante == 'S' \
                        or (years != 0 and years < 30) \
                        or (years != 0 and years > 45):
                    self.total_personas_insercion += 1
            visited_candidates.append(candidate.id_trabajador)

    def __interviews(self) -> None:
        interviews = self.__repository.get_interviews(self.__start_date, self.__end_date)
        self.total_ofertas_enviadas = len(interviews)

    def __call__(self) -> dict:
        print('fetch new candidates')
        self.__new_candidates()
        print('fetch deals n offers')
        self.__deals_n_offers()
        print('fetch interviews')
        self.__interviews()
        print('fetch candidates with colocation')
        self.__candidates_with_colocation()
        print('calculate total people')
        self.__total_people_count()
        print('summarize')
        self.__summarize()
        aggregated_info = self.to_dict()
        aggregated_info['Anho'] = self.__start_date.year
        aggregated_info['Mes'] = self.__start_date.month
        aggregated_info['Total_personas_receptores'] = aggregated_info['Total_personas_perceptores']
        return {
            'candidates': self.__candidates,
            'aggregated': aggregated_info
        }


if __name__ == '__main__':
    # from packages.adapters.zohoSDK.zoho_api_requests import ApiRequestRepository
    from packages.adapters.zohoSDK.zoho_api_requests import ApiRequestRepository

    repo = ApiRequestRepository()
    start = date(2022, 7, 1)
    end = date(2022, 7, 31)
    info = MonthlyInfo(start, end, repo)

    # print('Test new candidates')
    # info.new_candidates()
    # print(info.total_nuevas_registradas)

    # print('Test deals n offers')
    # info.deals_n_offers()

    # print('Test candidates with colocation')
    # info.candidates_with_colocation()
    # print(info.total_ofertas_cubiertas)

    # print('Test contract type')
    # info.contract_type()
    # print(info.total_contratos)
    # print(info.total_contratos_indefinidos)

    # print('Test interviews')
    # info.interviews()
    # print(info.total_ofertas_enviadas)
