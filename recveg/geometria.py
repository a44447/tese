# -*- coding: utf-8 -*-
"""
Geometria

@author: Rui Reis
"""
import ee
from .evento import Evento
from .gee import GEE

class Geometria:
    """Encapsula a funcionalidade de avaliação da geometria dos fogos ocorridos"""

    def __init__(self, identificador, tolerancia, distancia):
        self.__tolerancia = tolerancia
        self.__distancia = distancia
        self.__registo = Geometria.__gera_registo(identificador)
        self.__alvo = Geometria.__gera_alvo(self.__registo, tolerancia)
        self.__total = Geometria.__gera_total(self.__alvo, distancia)
        self.__referencia = self.__total\
            .difference(self.__alvo)\
            .simplify(tolerancia)
        self.__evento = None

    @classmethod
    def __gera_territorio(cls, pais, territorio):
        """
        Gera a representação da geometria de um território usando uma fonte
        de dados do Departamento de Estado dos Estados Unidos da América
        """
        return ee.FeatureCollection(GEE.LT_COLECCAO)\
            .filter(ee.Filter.And(\
                ee.Filter.eq(GEE.LT_CODIGO, pais),\
                ee.Filter.eq(GEE.LT_NOME, territorio)))\
            .geometry()

    @classmethod
    def __gera_registo(cls, identificador):
        """Gera a representação do registo do ICNF correspondente a um incêndio"""
        return ee.FeatureCollection(GEE.ICNF_COLECCAO)\
            .filter(ee.Filter.eq(GEE.ICNF_CAMPO_IDENTIFICADOR, identificador))\
            .first()

    @classmethod
    def __gera_alvo(cls, registo, tolerancia):
        """Gera a representação da geometria do incêndio"""
        geometria = registo.geometry()
        # Simplifica a geometria, dada uma tolerância
        if tolerancia > 0:
            geometria = geometria.simplify(tolerancia)
        return geometria

    @classmethod
    def __gera_total(cls, geometria, distancia):
        """
        Gera a representação da expansão da zona ardida numa largura
        definida pela distância linear indicada
        """
        # pylint: disable=E1101
        portugal = cls.__gera_territorio("PO", "Portugal")
        erro = ee.ErrorMargin(distancia, GEE.UNIDADES_METROS)

        # Alarga a geometria do incêndio, dada uma distância linear
        # e vamos garantir que excluímos zonas de mar junto à costa
        return geometria\
            .buffer(distancia, erro)\
            .intersection(portugal)

    @property
    def tolerancia(self):
        """Tolerância, em metros, a aplicar na simplificação da geometria"""
        return self.__tolerancia

    @property
    def distancia(self):
        """Distância correspondente à largura da faixa de referência"""
        return self.__distancia

    @property
    def evento(self):
        """Decrição do evento"""
        return self.__evento

    @property
    def alvo(self):
        """Geometria alvo do incêndio"""
        return self.__alvo

    @property
    def referencia(self):
        """Geometria de referência adjacente ao incêndio"""
        return self.__referencia

    @property
    def total(self):
        """Geometria total (alvo e referência)"""
        return self.__total

    def extrai(self):
        """Extrai informação do evento"""
        self.__evento = Evento(self.__registo.toDictionary(Evento.campos()).getInfo())
