class Candidate:
    def __init__(self, from_dict: dict):
        self.id_trabajador = from_dict.get('DNI_NIE_Permiso_de_trabajo')
        self.nombre_trabajador = from_dict.get('Nombre')
        self.apellido1_trabajador = from_dict.get('Apellidos')
        self.apellido2_trabajador = from_dict.get('Segundo_apellido_cuidador')
        self.fecha_nacimiento = from_dict.get('Fecha_de_Nacimiento')
        self.sexo_trabajador = from_dict.get('Sexo')
        self.discapacidad = from_dict.get('Indicador_discapacidad')
        self.inmigrante = from_dict.get('Indicador_inmigrante')
        self.nivel_formativo = from_dict.get('Nivel_formativo')
        if from_dict.get('Fecha_inicio_actividad') is not None:
            self.colocacion = 'S'
            self.fecha_colocacion = from_dict.get('Fecha_inicio_actividad')
            self.tipo_contrato = from_dict.get('Codigo_tipo_contrato_cuidador')
            self.cif_nif_empresa = from_dict.get('cif_nif_empresa')
            self.razon_social_empresa = from_dict.get('razon_social_empresa')
        else:
            self.colocacion = 'N'
        # no se exportan
        self.recibe_prestaciones_desempleo = from_dict.get('Indicador_recibe_prestaciones_desempleo')
        self.dificultades_insercion = from_dict.get('Indicador_colectivo_dificultades_insercion')
        self.fecha_nacimiento_iso_date = from_dict.get(
            'Fecha_de_Nacimiento_iso_date')  # se usa para calcular la edad, usada por el filtro de problemas de inserción

    def to_dict(self):

        response = {
            'id_trabajador': self.id_trabajador,
            'nombre_trabajador': self.nombre_trabajador,
            'apellido1_trabajador': self.apellido1_trabajador,
            'apellido2_trabajador': self.apellido2_trabajador,
            'fecha_nacimiento': self.fecha_nacimiento,
            'sexo_trabajador': self.sexo_trabajador,
            'nivel_formativo': self.nivel_formativo,
            'discapacidad': self.discapacidad,
            'inmigrante': self.inmigrante,
            'colocacion': self.colocacion,
        }
        if self.colocacion == 'S':
            response['fecha_colocacion'] = self.fecha_colocacion
            response['tipo_contrato'] = self.tipo_contrato
            response['cif_nif_empresa'] = self.cif_nif_empresa
            response['razon_social_empresa'] = self.razon_social_empresa

        return response

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id_trabajador == other.id_trabajador

    def __hash__(self):
        return hash(self.id_trabajador)
