# -*- coding: utf-8 -*-
"""
Caracterização de uma zona ardida na base de dados do ICNF

@author: Rui Reis
"""
from datetime import datetime
from .gee import GEE
from .utilidades import Utilidades

class Evento:
    """Encapsula a informação de um evento"""
    __FORMATO_DATA = "%Y-%m-%d"
    __FORMATO_STR = "%-16s:\t%s\n"

    def __init__(self, dados):
        self.__identificador = dados.get(GEE.ICNF_CAMPO_IDENTIFICADOR)
        self.__data_inicio = Evento.__icnf_data(dados.get(GEE.ICNF_CAMPO_INICIO))
        self.__data_fim = Evento.__icnf_data(dados.get(GEE.ICNF_CAMPO_FIM))
        self.__local = dados.get(GEE.ICNF_CAMPO_LOCAL)
        self.__freguesia = dados.get(GEE.ICNF_CAMPO_FREGUESIA)
        self.__concelho = dados.get(GEE.ICNF_CAMPO_CONCELHO)
        self.__distrito = dados.get(GEE.ICNF_CAMPO_DISTRITO)

    @classmethod
    def __icnf_data(cls, data):
        """Descodifica um campo de data do ICNF para um timestamp unix em milisegundos"""
        return datetime.strptime(data[0:10], cls.__FORMATO_DATA).timestamp() * 1e3

    @classmethod
    def campos(cls):
        """Devolve a lista dos nomes dos campos correspondentes ao evento"""
        return GEE.ICNF_CAMPOS

    @property
    def identificador(self):
        """Identificador do evento"""
        return self.__identificador

    @property
    def data_inicio(self):
        """Data inicio do fogo"""
        return self.__data_inicio

    @property
    def data_fim(self):
        """Data de extinção do fogo"""
        return self.__data_fim

    @property
    def local(self):
        """Nome do local onde ocorreu o fogo"""
        return self.__local

    @property
    def freguesia(self):
        """Freguesia onde pertence o local"""
        return self.__freguesia

    @property
    def concelho(self):
        """Concelho onde pertence a Freguesia"""
        return self.__concelho

    @property
    def distrito(self):
        """Distrito onde pertence o Concelho"""
        return self.__distrito

    def __str__(self):
        data_inicio = Utilidades.formata_data_hora(self.__data_inicio)
        data_fim = Utilidades.formata_data_hora(self.__data_fim)
        return (self.__FORMATO_STR % ("Identificador", self.__identificador))\
            +(self.__FORMATO_STR % ("Data início", data_inicio))\
            +(self.__FORMATO_STR % ("Data fim", data_fim))\
            +(self.__FORMATO_STR % ("Local", self.__local))\
            +(self.__FORMATO_STR % ("Freguesia", self.__freguesia))\
            +(self.__FORMATO_STR % ("Concelho", self.__concelho))\
            +(self.__FORMATO_STR % ("Distrito", self.__distrito))
