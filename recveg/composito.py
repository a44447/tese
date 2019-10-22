# -*- coding: utf-8 -*-
"""
Compósito MVC de NDVI

@author: Rui Reis
"""
import datetime
import ee
from .sentinel import Sentinel
from .gee import GEE

class Composito:
    """Compósito MVC de NDVI"""
    # Bandas
    __NDVI_AF = "NDVI_AF"
    __NDVI_AM = "NDVI_AM"
    __NDVI_AV = "NDVI_AV"
    __NDVI_RF = "NDVI_RF"
    __NDVI_RM = "NDVI_RM"
    __NDVI_RV = "NDVI_RV"
    # Constantes
    __BANDAS = "B"
    __REDUTOR = "R"
    __VALIDACAO = "%s_V"

    # Descrição dos campos
    CARACTERISTICAS = ["Data inicio",\
                       "Data fim",\
                       "Imagens",\
                       "Tempo de processamento (microsec)",\
                       "NDVI alvo floresta média",\
                       "NDVI referência floresta média",\
                       "NDVI alvo mato média",\
                       "NDVI referência mato média",\
                       "NDVI alvo vegetação média",\
                       "NDVI referência vegetação média",\
                       "NDVI alvo floresta mediana",\
                       "NDVI referência floresta mediana",\
                       "NDVI alvo mato mediana",\
                       "NDVI referência mato mediana",\
                       "NDVI alvo vegetação mediana",\
                       "NDVI referência vegetação mediana",\
                       "NDVI alvo floresta pontos",\
                       "NDVI referência floresta pontos",\
                       "NDVI alvo mato pontos",\
                       "NDVI referência mato pontos",\
                       "NDVI alvo vegetação pontos",\
                       "NDVI referência vegetação pontos"]
    # Campos de cada registo
    DATA_INICIO = 0
    DATA_FIM = 1
    IMAGENS = 2
    TEMPO_PROCESSAMENTO = 3
    NDVI_MEDIA_FLORESTA_ALVO = 4
    NDVI_MEDIA_FLORESTA_REFERENCIA = 5
    NDVI_MEDIA_MATO_ALVO = 6
    NDVI_MEDIA_MATO_REFERENCIA = 7
    NDVI_MEDIA_VEGETACAO_ALVO = 8
    NDVI_MEDIA_VEGETACAO_REFERENCIA = 9
    NDVI_MEDIANA_FLORESTA_ALVO = 10
    NDVI_MEDIANA_FLORESTA_REFERENCIA = 11
    NDVI_MEDIANA_MATO_ALVO = 12
    NDVI_MEDIANA_MATO_REFERENCIA = 13
    NDVI_MEDIANA_VEGETACAO_ALVO = 14
    NDVI_MEDIANA_VEGETACAO_REFERENCIA = 15
    NDVI_PONTOS_FLORESTA_ALVO = 16
    NDVI_PONTOS_FLORESTA_REFERENCIA = 17
    NDVI_PONTOS_MATO_ALVO = 18
    NDVI_PONTOS_MATO_REFERENCIA = 19
    NDVI_PONTOS_VEGETACAO_ALVO = 20
    NDVI_PONTOS_VEGETACAO_REFERENCIA = 21

    def __init__(self, data, modelo, dias=10):
        # Variáveis retiradas do modelo
        self.__modelo = modelo
        # Variáveis internas
        self.__processamento = None
        self.__metricas = None
        self.__sumario = None
        # Representação da data inicio e data fim do intervalo recebidas como
        # timestamps de unix em milisegundos
        self.__inicio = ee.Date(data)
        self.__fim = ee.Date(data).advance(dias, "day")

    @classmethod
    def palette(cls):
        """Palette de cores para visualização de NDVI"""
        return [\
            "FFFFFF", "CE7E45", "DF923D", "F1B555", "FCD163", "99B718",\
            "74A901", "66A000", "529400", "3E8601", "207401", "056201",\
            "004C00", "023B01", "012E01", "011D01", "011301"]

    @property
    def inicio(self):
        """Data inicio do compósito"""
        self.__verifica()
        if self.imagens > 1:
            return self.__sumario["values"]["min"]
        # Mínimo e máximo não vêm preenchidos com uma imagem
        return self.__sumario["values"]["sum"]

    @property
    def fim(self):
        """Data fim do compósito"""
        self.__verifica()
        if self.imagens > 1:
            return self.__sumario["values"]["max"]
        # Mínimo e máximo não vêm preenchidos com uma imagem
        return self.__sumario["values"]["sum"]

    @property
    def inicio_intervalo(self):
        """Data inicio do intervalo"""
        return self.__inicio.getInfo()["value"]

    @property
    def fim_intervalo(self):
        """Data fim do intervalo"""
        return self.__fim.getInfo()["value"]

    @property
    def imagens(self):
        """Número de imagens no compósito"""
        self.__verifica()
        return self.__sumario["values"]["total_count"]

    @property
    def processamento(self):
        """Obtem a tempo de processamento para este compósito"""
        self.__verifica()
        return self.__processamento

    @property
    def metricas(self):
        """Obtem as metricas para este compósito"""
        self.__verifica()
        return self.__metricas

    @property
    def alvo(self):
        """Cobertura da área alvo"""
        return self.__modelo.alvo

    @property
    def referencia(self):
        """Cobertura da área de referência"""
        return self.__modelo.referencia

    @property
    def perimetro(self):
        """Perimetro da área total"""
        return self.__modelo.geometria.total

    @property
    def escala(self):
        """Escala da cobertura de superfície"""
        return self.__modelo.escala

    @property
    def caracteristicas(self):
        """Lista das carecterísticas do registo posicional do composto"""
        return self.CARACTERISTICAS

    @property
    def registo(self):
        """Obtem o registo posicional deste composto"""
        if self.metricas is None:
            return None

        return [\
            self.inicio,\
            self.fim,\
            self.imagens,\
            self.processamento]+\
            [self.metricas[0]["properties"][m] for m in self.__bandas_ndvi]+\
            [self.metricas[1]["properties"][m] for m in self.__bandas_ndvi]+\
            [self.metricas[2]["properties"][m] for m in self.__bandas_validacao]

    @property
    def __bandas_ndvi(self):
        """Lista das bandas de NDVI"""
        return [\
                self.__NDVI_AF, self.__NDVI_RF,\
                self.__NDVI_AM, self.__NDVI_RM,\
                self.__NDVI_AV, self.__NDVI_RV]

    @property
    def __bandas_validacao(self):
        """Lista das bandas de validação"""
        return [self.__VALIDACAO % (x) for x in self.__bandas_ndvi]

    def __verifica(self):
        """Verifica a disponibilidade dos parâmetros que necessitam de avaliação no GEE"""
        if self.__sumario is None:
            raise RuntimeError(u"Antes de usar o objecto, terá que o inicializar")

    def __gera_metricas(self):
        """
        Gera a representação da lista de redutores para agregar as métricas
        de NDVI para este MVC
        """
        # pylint: disable=E1101
        # Nomes das bandas de NDVI e validação
        bandas_ndvi = ee.List(self.__bandas_ndvi)
        bandas_validacao = ee.List(self.__bandas_validacao)
        # Redutores
        medias = ee.Dictionary(\
            {self.__BANDAS: bandas_ndvi, self.__REDUTOR: ee.Reducer.mean()})
        medianas = ee.Dictionary(\
            {self.__BANDAS: bandas_ndvi, self.__REDUTOR: ee.Reducer.median()})
        contagens = ee.Dictionary(
            {self.__BANDAS: bandas_validacao, self.__REDUTOR: ee.Reducer.sum()})
        return ee.List([medias, medianas, contagens])

    def __gera_ndvi(self, composito):
        """Gera a repreentação dos mapeamentos das bandas de NDVI"""
        return composito\
            .map(Sentinel.mapa_ndvi(self.__NDVI_AF, self.alvo.floresta.imagem))\
            .map(Sentinel.mapa_ndvi(self.__NDVI_AM, self.alvo.mato.imagem))\
            .map(Sentinel.mapa_ndvi(self.__NDVI_AV, self.alvo.vegetacao.imagem))\
            .map(Sentinel.mapa_ndvi(self.__NDVI_RF, self.referencia.floresta.imagem))\
            .map(Sentinel.mapa_ndvi(self.__NDVI_RM, self.referencia.mato.imagem))\
            .map(Sentinel.mapa_ndvi(self.__NDVI_RV, self.referencia.vegetacao.imagem))

    def __gera_validacao(self, composito):
        """Gera a representação dos mapeamentos para bandas de validação"""
        # pylint: disable=R0201
        return composito\
            .map(Sentinel.mapa_validacao(self.__NDVI_AF))\
            .map(Sentinel.mapa_validacao(self.__NDVI_AM))\
            .map(Sentinel.mapa_validacao(self.__NDVI_AV))\
            .map(Sentinel.mapa_validacao(self.__NDVI_RF))\
            .map(Sentinel.mapa_validacao(self.__NDVI_RM))\
            .map(Sentinel.mapa_validacao(self.__NDVI_RV))

    def __mapa_metricas(self, geometria, escala, imagem):
        """Mapeamento e avaliação das métricas"""
        # pylint: disable=R0201
        def __funcao_metricas(metrica):
            objecto = ee.Dictionary(metrica)
            return ee.Feature(None, imagem\
                .select(objecto.get(self.__BANDAS))\
                .reduceRegion(\
                    reducer=objecto.get(self.__REDUTOR),
                    geometry=geometria,
                    scale=escala,
                    maxPixels=1e9))
        return __funcao_metricas

    def avalia(self):
        """Avalia o compósito de MVC"""
        # Timestamp do inicio
        inicio = datetime.datetime.now()
        coleccao = Sentinel.coleccao(self.perimetro, self.__inicio, self.__fim)
        self.__sumario = coleccao\
            .aggregate_stats(GEE.IMAGEM_DATA)\
            .getInfo()
        lista = self.__gera_metricas()
        composito = self.__gera_ndvi(coleccao)
        composito = self.__gera_validacao(composito)
        composito = composito\
            .select(self.__bandas_ndvi+self.__bandas_validacao)\
            .max()
        if self.imagens > 0:
            self.__metricas = lista\
                .map(self.__mapa_metricas(self.perimetro, self.escala, composito))\
                .getInfo()
        # Timestamp do final do processo
        self.__processamento = (datetime.datetime.now()-inicio).microseconds
