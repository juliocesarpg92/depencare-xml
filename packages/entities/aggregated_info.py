class AggregatedInfo:
    def __init__(self):
        self.total_personas = 0
        self.total_nuevas_registradas = 0
        self.total_personas_perceptores = 0
        self.total_personas_insercion = 0
        self.total_ofertas = 0
        self.total_ofertas_enviadas = 0
        self.total_ofertas_cubiertas = 0
        self.total_puestos = 0
        self.total_puestos_cubiertos = 0
        self.total_contratos = 0
        self.total_contratos_indefinidos = 0
        self.total_personas_colocadas = 0

    def to_dict(self):
        return {
            'Total_personas': self.total_personas,
            'Total_nuevas_registradas': self.total_nuevas_registradas,
            'Total_personas_perceptores': self.total_personas_perceptores,
            'Total_personas_insercion': self.total_personas_insercion,
            'Total_ofertas': self.total_ofertas,
            'Total_ofertas_enviadas': self.total_ofertas_enviadas,
            'Total_ofertas_cubiertas': self.total_ofertas_cubiertas,
            'Total_puestos': self.total_puestos,
            'Total_puestos_cubiertos': self.total_puestos_cubiertos,
            'Total_contratos': self.total_contratos,
            'Total_contratos_indefinidos': self.total_contratos_indefinidos,
            'Total_personas_colocadas': self.total_personas_colocadas
        }
