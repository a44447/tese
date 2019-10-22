# -*- coding: utf-8 -*-
"""
Cobertura - Corine Land Cover

@author: Rui Reis
"""
import ee
from .gee import GEE

class Cobertura:
    """
    Classe que encapsula a funcionalidade de caracterização da cobertura da
    superfície terrestre tendo em conta a utilização do Corinne Land Cover
    (CLC) publicado pela plataforma Copernicus
    """
    class Floresta:
        """Categorias de CLC para tipos de floresta"""
        # pylint: disable=R0903
        Folhosas = 23
        Coniferas = 24
        Mista = 25

        @classmethod
        def lista(cls):
            """Lista das categorias CLC para tipos de floresta"""
            return [cls.Folhosas, cls.Coniferas, cls.Mista]

    class Mato:
        """Lista das categorias CLC para tipos de mato"""
        # pylint: disable=R0903
        Prado = 26
        Charneca = 27
        Pasto = 28
        Arbusto = 29

        @classmethod
        def lista(cls):
            """Lista das categorias CLC para tipos de mato"""
            return [cls.Prado, cls.Charneca, cls.Pasto, cls.Arbusto]

    @classmethod
    def palette(cls):
        """Palette de cores para visualização de classes CLC"""
        return [\
            "FFFFFF", "E6004D", "FF0000", "CC4DF2", "CC0000", "E6CCCC",\
            "E6CCE6", "A600CC", "A64DCC", "FF4DFF", "FFA6FF", "FFE6FF",\
            "FFFFA8", "FFFF00", "E6E600", "E68000", "F2A64D", "E6A600",\
            "E6E64D", "FFE6A6", "FFE64D", "E6CC4D", "F2CCA6", "80FF00",\
            "00A600", "4DFF00", "CCF24D", "A6FF80", "A6E64D", "A6F200",\
            "E6E6E6", "CCCCCC", "CCFFCC", "000000", "A6E6CC", "A6A6FF",\
            "4D4DFF", "CCCCFF", "E6E6FF", "A6A6E6", "00CCF2", "80F2E6",\
            "00FFA6", "A6FFE6", "E6F2FF"]

    @classmethod
    def lista(cls):
        """Lista das categorias CLC para tipos de vegetação"""
        return cls.Floresta.lista() + cls.Mato.lista()

    @classmethod
    def gera(cls, regiao, categorias=None):
        """
        Gera uma representação da imagem correspondente ao Corine Land
        Cover  de 2012 para a região indicada
        """
        # Garantir a unicidade da imagem e recortar a área
        imagem = ee.ImageCollection(GEE.CLC_COLECCAO)\
            .filter(ee.Filter.eq(GEE.IMAGEM_INDICE, GEE.CLC_ANO))\
            .first()\
            .clip(regiao)

        if categorias is not None:
            expressao = ""
            # pylint: disable=C0200
            for index in range(0, len(categorias)):
                if index != 0:
                    expressao += " || "
                expressao += "clc==" + str(categorias[index])

        # Seleciona as categorias indicadas
        imagem = imagem.expression(expressao, {"clc": imagem.select(GEE.CLC_BANDA)})

        # Apenas queremos saber se existe uma das categorias
        return imagem
