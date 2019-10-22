# -*- coding: utf-8 -*-
"""
Constantes GEE e das suas fontes de dados

@author: Rui Reis
"""

class GEE:
    """Constantes do GEE"""
    #pylint: disable=R0903
    # Propriedades
    IMAGEM_INDICE = "system:index"
    IMAGEM_DATA = "system:time_start"
    # Sentinel 2
    # Bandas
    BANDA_QUALIDADE = "QA60"
    BANDA_NIR = "B8"
    BANDA_RED = "B4"
    # Propriedades e nomes
    SENTINEL_COLECCAO = "COPERNICUS/S2"
    SENTINEL_PERCENTAGEM_NUVENS = "CLOUDY_PIXEL_PERCENTAGE"
    # Outros
    UNIDADES_METROS = "meters"
    #Corine Land Cover
    CLC_COLECCAO = "COPERNICUS/CORINE/V18_5_1/100m"
    CLC_ANO = "2012"
    CLC_BANDA = "landcover"
    # Limite territorial do USDOS
    LT_COLECCAO = "USDOS/LSIB_SIMPLE/2017"
    LT_CODIGO = "country_co"
    LT_NOME = "country_na"
    # ICNF
    # ATENCÃO: Este nome depende do nome atribuido pelo developer ao ficheiro
    # com a informação do ICNF
    ICNF_COLECCAO = "users/ruisreis/AreasArdidas-2017-031002018-ETRS89PTTM06"
    # Nomes dos campos de informação
    ICNF_CAMPO_IDENTIFICADOR = "Cod_SGIF"
    ICNF_CAMPO_INICIO = "DHInicio"
    ICNF_CAMPO_FIM = "DHFim"
    ICNF_CAMPO_LOCAL = "Local"
    ICNF_CAMPO_FREGUESIA = "Freguesia"
    ICNF_CAMPO_CONCELHO = "Concelho"
    ICNF_CAMPO_DISTRITO = "Distrito"
    ICNF_CAMPOS = [ICNF_CAMPO_IDENTIFICADOR, ICNF_CAMPO_INICIO, ICNF_CAMPO_FIM,\
                   ICNF_CAMPO_LOCAL, ICNF_CAMPO_FREGUESIA, ICNF_CAMPO_CONCELHO,\
                   ICNF_CAMPO_DISTRITO]
