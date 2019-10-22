# -*- coding: utf-8 -*-
"""
Dados multi-espectrais da missão Sentinel 2

@author: Rui Reis
"""
import ee
from .gee import GEE

class Sentinel:
    """Obtenção de dados do Sentinel 2"""
    # pylint: disable=R0903
    # Percentagem de cobertura máxima de nuvens
    __PERCENTAGEM_NUVENS = 20

    @classmethod
    def coleccao(cls, regiao, inicio, fim):
        """
        Obtém uma colecção de imagens do Sentinel 2 incluindo apenas as
        imagens com menos de 20% de nuvens na região seleccionada para o
        intervalo entre as datas de inicio e fim
        """
        return ee.ImageCollection(GEE.SENTINEL_COLECCAO)\
            .filter(ee.Filter.And(\
                ee.Filter.lt(GEE.SENTINEL_PERCENTAGEM_NUVENS, cls.__PERCENTAGEM_NUVENS),\
                ee.Filter.geometry(regiao),\
                ee.Filter.date(inicio, fim)))

    @classmethod
    def mapa_ndvi(cls, nome, cobertura):
        """
        Função de mapeamento para geração das bandas de NDVI com exclusão
        das zonas afetadas por nuvens
        """
        def __funcao_ndvi(imagem):
            return imagem.addBands(ee.Image(imagem\
                    .updateMask(cobertura)\
                    .updateMask(\
                        imagem.select(GEE.BANDA_QUALIDADE).bitwiseAnd(1 << 10).eq(0)\
                            .And(imagem.select(GEE.BANDA_QUALIDADE).bitwiseAnd(1 << 11).eq(0)))\
                    .normalizedDifference([GEE.BANDA_NIR, GEE.BANDA_RED])\
                    .float()\
                    .rename(nome))\
                .copyProperties(imagem, [GEE.IMAGEM_DATA]))
        return __funcao_ndvi

    @classmethod
    def mapa_validacao(cls, nome):
        """Map que adiciona uma banda com o sufixo _B que representa os pixeis válidos"""
        def __funcao__validacao(imagem):
            return imagem.addBands(imagem.select(nome).gt(0).rename(nome + "_V"))
        return __funcao__validacao
    