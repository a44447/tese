# -*- coding: utf-8 -*-
"""
Encapsula a base de dados de zonas ardidas da base de dados do ICNF

@author: Rui Reis
"""
import ee
from .gee import GEE
from .evento import Evento

class ZonasArdidas:
    """Extrai informação descritiva das zonas ardidas"""

    def __init__(self):
        self.__lista = None
        self.__distrito = None
        self.__concelho = None
        self.__freguesia = None
        self.__local = None

    @property
    def lista(self):
        """Lista de descrições de zonas ardidas em bruto"""
        return self.__lista

    @property
    def eventos(self):
        """Lista das zonas ardidas sob a forma de uma lista de objectos Evento"""
        return [Evento(zona) for zona in self.__lista]

    @classmethod
    def __por_cada(cls, campos):
        """Função mapa para tratamento de registos"""
        # pylint: disable=R0201
        def __itera(registo, lista):
            return ee.List(lista).add(registo.toDictionary(campos))
        return __itera

    @classmethod
    def __gera_filtro(cls, coleccao, campo, valor):
        """Gera a representação de um filtro de igualdade no GEE"""
        if valor is None:
            return coleccao
        return coleccao.filter(ee.Filter.eq(campo, ee.String(valor)))

    def distritos(self):
        """Obtém uma lista de Distritos com a indicação do número de eventos associado a cada um"""
        # pylint: disable=R0201
        return ee.FeatureCollection(GEE.ICNF_COLECCAO)\
            .aggregate_histogram(GEE.ICNF_CAMPO_DISTRITO)\
            .getInfo()

    def extrai(self, distrito=None, concelho=None, freguesia=None, local=None):
        """Extrai os eventos de acordo com o critério apresentado"""
        if distrito is None and concelho is None and freguesia is None and local is None:
            raise AttributeError("Pelo menos um dos critérios tem que ser indicado")
        registos = ee.FeatureCollection(GEE.ICNF_COLECCAO)
        registos = self.__gera_filtro(registos, GEE.ICNF_CAMPO_DISTRITO, self.__distrito)
        registos = self.__gera_filtro(registos, GEE.ICNF_CAMPO_CONCELHO, self.__concelho)
        registos = self.__gera_filtro(registos, GEE.ICNF_CAMPO_FREGUESIA, self.__freguesia)
        registos = self.__gera_filtro(registos, GEE.ICNF_CAMPO_LOCAL, self.__local)
        buffer = registos.iterate(self.__por_cada(Evento.campos()), ee.List([]))
        self.__lista = buffer.getInfo()
        return self.__lista
