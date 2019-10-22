# -*- coding: utf-8 -*-
"""
Modelo de extração, agregação e armazenamento de dados

@author: Rui Reis
"""
import os
import pickle
import ee
import numpy

from .geometria import Geometria
from .sentinel import Sentinel
from .modelocobertura import ModeloCobertura
from .composito import Composito
from .gee import GEE
from .utilidades import Utilidades

class ModeloNotificacao:
    """Classe que suporta as notificações ao processo do utilizador e o fluxo"""
    INICIO = 0
    SUCESSO = 1
    VAZIO = 2
    TERMINA = 3

    """Classe que encapsula as notificações de eventos ocorrdos no modelo"""
    def __init__(self, evento=None):
        self.__evento = evento
        self.__fluxo = True

    @property
    def fluxo(self):
        """Estado do fluxo de execução"""
        return self.__fluxo

    def __notifica(self, tipo, dados=None):
        """Notificação base do processo do utilizador"""
        if self.__evento is not None:
            self.__fluxo = self.__fluxo and self.__evento(dados, tipo)
        return self.__fluxo

    def inicio(self, dados=None):
        """Notifica o processo do utilizador que iniciou a avaliação de um MVC"""
        return self.__notifica(self.INICIO, dados)

    def sucesso(self, dados=None):
        """Notifica o processo do utilizador que foi avaliado um MVC válido"""
        return self.__notifica(self.SUCESSO, dados)

    def vazio(self, dados=None):
        """Notifica o processo do utilizador que não existe MVC na data"""
        return self.__notifica(self.VAZIO, dados)

    def termina(self):
        """O fluxo foi terminado, modifica o estado"""
        self.__fluxo = False
        return self.__notifica(self.TERMINA)

class Modelo:
    """Modelo de exploração, agregação e persistência dos dados de GEE"""
    # Nomes dos campos usado no ficheiro
    COMUM_FF = "comum"
    VERSAO_FF = "versao"
    LOCAL_FF = "local"
    TOLERANCIA_FF = "tolerancia"
    ADJACENTE_FF = "adjacente"
    ESCALA_FF = "escala"
    DATA_INCENDIO_FF = "data_incendio"
    DATA_PRIMEIRA_IMAGEM_FF = "data_prineira_imagem"
    COMUM_FL = [VERSAO_FF, LOCAL_FF, TOLERANCIA_FF, ADJACENTE_FF,\
                DATA_INCENDIO_FF, DATA_PRIMEIRA_IMAGEM_FF]
    ALVO_FF = "alvo"
    FLORESTA_FF = "floresta"
    MATO_FF = "mato"
    VEGETACAO_FF = "vegetacao"
    ALVO_FL = [ESCALA_FF, FLORESTA_FF, MATO_FF, VEGETACAO_FF]
    REFERENCIA_FF = "referencia"
    REFERENCIA_FL = [ESCALA_FF, FLORESTA_FF, MATO_FF, VEGETACAO_FF]
    TABELA_FF = "tabela"
    METADADOS_FF = "metadados"

    def __init__(self, local, tolerancia=100, distancia=300, ciclo=10):
        self.__geometria = Geometria(local, tolerancia, distancia)
        self.__ciclo = ciclo
        self.__data_primeira_imagem = None
        self.__alvo = None
        self.__referencia = None
        self.__escala = None
        self.__tabela = None

    def inicializa(self):
        """Inicializa o modelo"""
        if self.__alvo is None:
            self.__geometria.extrai()
            self.__alvo = ModeloCobertura(self.__geometria.alvo)
            self.__referencia = ModeloCobertura(self.__geometria.referencia)
            self.__data_primeira_imagem = self.__avalia_primeira_imagem(self.evento.data_inicio)

    def __avalia_primeira_imagem(self, data):
        """Avalia a data da primeira imagem válida após a data indicada"""
        nova_data = None
        imagens = Sentinel.coleccao(self.geometria.total,\
            ee.Date(data),\
            ee.Date(Utilidades.agora()))
        if imagens.size().getInfo() > 0:
            imagem = imagens.first()
            # Subsidiáriamente, avalia a escala se ainda não existir
            self.__avalia_escala(imagem)
            nova_data = imagem.get(GEE.IMAGEM_DATA).getInfo()
        return nova_data

    def __avalia_escala(self, imagem):
        """Avalia a escala da banda RED"""
        if self.__escala is None and imagem is not None:
            self.__escala = imagem\
                .select(GEE.BANDA_RED)\
                .projection()\
                .nominalScale()\
                .getInfo()
                
    def __proxima_data(self, data):
        """Data do próximo compósito"""
        proxima_data = Utilidades.dia_seguinte(Utilidades.dia_apos(data, self.__ciclo))
        if data >= Utilidades.apenas_data(Utilidades.agora()):
            proxima_data = None
        return proxima_data

    def __verifica(self):
        """Método de verificação da inicialização"""
        if self.__alvo is None or self.__referencia is None:
            raise RuntimeError(u"Antes de usar o objecto, terá que o inicializar")

    @property
    def versao(self):
        """Versão do modelo"""
        return "1.0"

    @property
    def evento(self):
        """Identificador do incêndio"""
        self.__verifica()
        return self.__geometria.evento

    @property
    def tolerancia(self):
        """Tolerância, em metros, a aplicar na simplificação da geometria"""
        self.__verifica()
        return self.__geometria.tolerancia

    @property
    def distancia(self):
        """Distância correspondente à largura da faixa de referência"""
        self.__verifica()
        return self.__geometria.distancia

    @property
    def escala(self):
        """Escala da informação de NDVI em metros"""
        self.__verifica()
        return self.__escala

    @property
    def alvo(self):
        """Informação da cobertura na zona do incêndio"""
        self.__verifica()
        return self.__alvo

    @property
    def referencia(self):
        """Informação da cobertura na zona adjacente ao incêndio"""
        self.__verifica()
        return self.__referencia

    @property
    def geometria(self):
        """Geometria da área ardida (alvo e referência)"""
        self.__verifica()
        return self.__geometria

    @property
    def data_primeira_imagem(self):
        """Data da primeira imagem após o incêndio"""
        self.__verifica()
        return self.__data_primeira_imagem

    @property
    def tabela(self):
        """Tabela com os registos já avaliados"""
        if self.__tabela is None:
            self.__verifica()
        return self.__tabela

    def __mapa_guarda(self):
        """Mapeia as propriedades do objecto para uma colecção"""
        return {self.COMUM_FF: {self.VERSAO_FF: self.versao,\
                                 self.LOCAL_FF: self.evento.identificador,\
                                 self.TOLERANCIA_FF: self.tolerancia,\
                                 self.ADJACENTE_FF: self.distancia,\
                                 self.ESCALA_FF: self.escala,\
                                 self.DATA_INCENDIO_FF: self.evento.data_inicio,\
                                 self.DATA_PRIMEIRA_IMAGEM_FF: self.__data_primeira_imagem},\
                self.ALVO_FF: {self.ESCALA_FF: self.alvo.escala,\
                               self.FLORESTA_FF : self.alvo.floresta.dimensao,\
                               self.MATO_FF: self.alvo.mato.dimensao,\
                               self.VEGETACAO_FF: self.alvo.vegetacao.dimensao},\
                self.REFERENCIA_FF: {self.ESCALA_FF: self.referencia.escala,\
                                     self.FLORESTA_FF: self.referencia.floresta.dimensao,\
                                     self.MATO_FF: self.referencia.mato.dimensao,\
                                     self.VEGETACAO_FF: self.referencia.vegetacao.dimensao},\
                self.TABELA_FF: self.__tabela,\
                self.METADADOS_FF: {self.COMUM_FF: self.COMUM_FL,\
                                    self.ALVO_FF: self.ALVO_FL,\
                                    self.REFERENCIA_FF: self.REFERENCIA_FL,\
                                    self.TABELA_FF: Composito.CARACTERISTICAS}}

    def __mapa_carrega(self, coleccao):
        """Mapeia os dados de uma colecção para os campos do objecto"""
        # TODO: Detetar se algum dos parâmetros (local, tolerância, distância, etc...)
        # que possa afetar a coerência dos dados mudou, e neste caso lançar uma
        # exceção ou resolver a incoerência
        self.__tabela = coleccao[self.TABELA_FF]

    def __insere_composito(self, composito):
        """Insere um compósito MVC na tabela interna"""
        if self.__tabela is None:
            # A tabela ainda não tem dados, inicializa-a
            self.__tabela = numpy.array(composito.registo)
        else:
            # Adiciona uma linha à tabela existente
            self.__tabela = numpy.vstack((self.__tabela, composito.registo))

    def avalia(self, data_inicio=None, maximo=100, evento=None):
        """
        Avalia os compostos de NDVI, num máximo de compostos e
        reporta cada passo a evento
        """
        self.__verifica()
        notificacao = ModeloNotificacao(evento)
        agora = Utilidades.agora()
        contagem = 0
        if self.tabela is not None:
            # A tabela já existe, vamos atualizar os dados a partir da última data
            data = Utilidades.dia_seguinte(max(self.tabela[:, 1]))
        else:
            # A data da primeira imagem a avaliar é o argumento ou é determinada na inicialização
            if data_inicio is None:
                data = self.data_primeira_imagem
            else:
                data = data_inicio

        # Avalia até ser atingido o limite de imagens máximo, o fluxo ser quebrado
        # pelo processo do cliente ou a data de avaliação ser superior à data atual
        while contagem < maximo and notificacao.fluxo and data < agora:
            # Dispara o evento se existir
            notificacao.inicio(data)

            # Se não foi interrompido, prosssegue
            if notificacao.fluxo:
                # Avalia o MVC para a data (retira a hora do dia)
                data = Utilidades.apenas_data(data)
                composito = Composito(data, self, self.__ciclo)
                composito.avalia()
                if composito.imagens == 0:
                    # Não existe composto, determina a próxima data na colecção
                    # com uma imagem válida
                    notificacao.vazio(contagem)
                    #data = self.__avalia_primeira_imagem(data)
                    data = self.__proxima_data(data)
                    if data is None:
                        # Não existe próxima imagem, sai do ciclo
                        notificacao.termina()
                else:
                    # Insere o novo compósito na tabela
                    self.__insere_composito(composito)
                    notificacao.sucesso(composito)
                    # A próxima data a avaliar é o dia seguinte à última imagem
                    data = Utilidades.dia_seguinte(composito.fim_intervalo)
                contagem = contagem + 1

    def guarda(self, nome, esmaga=False):
        """Guarda o modelo num ficheiro"""
        if nome is not None and isinstance(nome, str) and nome:
            if os.path.isfile(nome):
                if not esmaga:
                    raise OSError(u"O ficheiro já existe, force o parâmetro esmaga")
        else:
            raise ValueError("O nome do ficheiro tem que ser indicado")
        ficheiro = open(nome, "wb")
        pickle.dump(self.__mapa_guarda(), ficheiro)
        ficheiro.close()

    def carrega(self, nome):
        """Carrega os dados de modelo a partir de um ficheiro"""
        if nome is not None and isinstance(nome, str) and nome:
            if not os.path.isfile(nome):
                raise OSError(u"O ficheiro não existe.")
            ficheiro = open(nome, "rb")
            dados = pickle.load(ficheiro, encoding='latin1')
            self.__mapa_carrega(dados)
        else:
            raise ValueError("O nome do ficheiro tem que ser indicado")
