# -*- coding: utf-8 -*-
"""
Modelo de cobertura

@author: Rui Reis
"""
from __future__ import absolute_import
import ee
from .cobertura import Cobertura
from .modelotipocobertura import ModeloTipoCobertura
from .gee import GEE

class ModeloCobertura:
    """Modela a cobertura de uma dada área definida pela geometria"""

    def __init__(self, geometria):
        self.__geometria = geometria
        self.__floresta = ModeloTipoCobertura(\
                Cobertura.gera(geometria, Cobertura.Floresta.lista()))
        self.__mato = ModeloTipoCobertura(\
                Cobertura.gera(geometria, Cobertura.Mato.lista()))
        self.__vegetacao = ModeloTipoCobertura(\
                Cobertura.gera(geometria, Cobertura.lista()))
        self.__escala = 0
        self.__dimensoes = None

    @property
    def geometria(self):
        """Geometria da zona"""
        return self.__geometria

    @property
    def floresta(self):
        """Modelo da cobertura de floresta"""
        return self.__floresta

    @property
    def mato(self):
        """Modelo da cobertura de mato"""
        return self.__mato

    @property
    def vegetacao(self):
        """Modelo da cobertura de vegetação"""
        return self.__vegetacao

    @property
    def escala(self):
        """Escala da informação da cobertura, usa a floresta como referência (*)"""
        if self.__escala == 0:
            self.__escala = self.floresta\
            .imagem\
            .projection()\
            .nominalScale()\
            .getInfo()
        return self.__escala

    @classmethod
    def __mapa_dimensao(self, geometria, escala):
        """Função de mapeamento para obtenção das dimensões dos modelos"""
        # pylint: disable=R0201
        def __funcao_dimensao(imagem):
            # pylint: disable=E1101
            return ee.Image(imagem).reduceRegion(\
                           reducer=ee.Reducer.sum(),\
                           geometry=geometria,\
                           scale=escala,\
                           maxPixels=1e9)
        return __funcao_dimensao

    def avalia(self):
        """Obtem a dimensão, em pontos, de cada máscara (*)"""
        if self.__dimensoes is None:
            lista = ee.List([self.floresta.imagem, self.mato.imagem, self.vegetacao.imagem])\
                .map(self.__mapa_dimensao(self.geometria, self.escala))\
                .getInfo()
            self.__dimensoes = lista
            self.__floresta = ModeloTipoCobertura(self.__floresta.imagem, lista[0][GEE.CLC_BANDA])
            self.__mato = ModeloTipoCobertura(self.__mato.imagem, lista[1][GEE.CLC_BANDA])
            self.__vegetacao = ModeloTipoCobertura(self.__vegetacao.imagem, lista[2][GEE.CLC_BANDA])
        return self.__dimensoes

    def imprime(self, titulo=None):
        """Envia para a consola um resumo do modelo de cobertura"""
        formato_mt = "%-16s:\t%6dm"
        formato_px = "%-16s:\t%6dpx"
        if titulo is not None:
            print(titulo)
        print(formato_mt % (u"Escala", self.escala))
        print(formato_px % (u"Floresta", self.floresta.dimensao))
        print(formato_px % (u"Mato«", self.mato.dimensao))
        print(formato_px % (u"Vegetação", self.vegetacao.dimensao))
