# -*- coding: utf-8 -*-
"""
Análise de sensibilidade

@author: Rui Reis
"""

import pickle
import numpy as np
import matplotlib.pyplot as plt
from recveg import Composito, Utilidades
from recveg.calculo import SerieHarmonica

# ==========
# Constantes
# ==========
# Dimensão das fontes de texto
FONTE_NORMAL = 32
FONTE_PEQUENA = 24
# Espaco entre elementos
ESPACO = 24

def executa_calculo(nome_ficheiro):
    """
    Executa o cálculo das séries harmónicas, apresenta as estatísticas e
    produz o gráfico para as subcategorias de vegetação usados na análise
    de sensibilidade
    """
    ficheiro = open(nome_ficheiro, "rb")
    modelo = pickle.load(ficheiro, encoding='latin1')
    dados = modelo["tabela"]

    tempo = dados[:, Composito.DATA_FIM].reshape(-1, 1)
    tempo = (tempo - tempo[0]) / Utilidades.DIA
    imagens = dados[:, Composito.IMAGENS]
    diametro = float(320) / (float(max(imagens) - min(imagens)) + 1)
    alvo = np.array(dados[:, Composito.NDVI_MEDIA_VEGETACAO_ALVO]).reshape(-1, 1)
    referencia = np.array(dados[:, Composito.NDVI_MEDIA_VEGETACAO_REFERENCIA]).reshape(-1, 1)
    serie_alvo = SerieHarmonica(tempo, alvo, ciclo=365)
    serie_referencia = SerieHarmonica(tempo, referencia, ciclo=365)

    plt.figure(1, figsize=(16, 10))
    plt.style.use("seaborn-darkgrid")
    plt.title(u"Área ardida", fontsize=FONTE_NORMAL, pad=ESPACO)
    plt.xlabel(u"Dias após o incêndio (t)", fontsize=FONTE_NORMAL)
    plt.ylabel("NDVI", fontsize=FONTE_NORMAL)
    plt.xticks(fontsize=FONTE_NORMAL)
    plt.yticks(fontsize=FONTE_NORMAL)
    plt.scatter(tempo, dados[:, Composito.NDVI_MEDIA_FLORESTA_ALVO], c="white",\
        edgecolor="red", s=92, lw=2, alpha=0.8, label=u"Floresta")
    plt.scatter(tempo, dados[:, Composito.NDVI_MEDIA_MATO_ALVO], c="white", \
        edgecolor="blue", s=92, lw=2, alpha=0.8, label=u"Mato")
    plt.scatter(tempo, alvo, c="green", s=imagens * diametro, alpha=0.5, label=u"Vegetação")
    serie_alvo.desenha(cor="orange", nome=u"Regressão")
    plt.legend(loc=2, fancybox=True, frameon=True, shadow=True, fontsize=FONTE_NORMAL)
    plt.show()
    serie_alvo.relatorio()

    plt.figure(2, figsize=(16, 10))
    plt.style.use("seaborn-darkgrid")
    plt.title(u"Área de referência", fontsize=FONTE_NORMAL, pad=ESPACO)
    plt.xlabel(u"Dias após o incêndio (t)", fontsize=FONTE_NORMAL)
    plt.ylabel("$NDVI^*$", fontsize=FONTE_NORMAL)
    plt.xticks(fontsize=FONTE_NORMAL)
    plt.yticks(fontsize=FONTE_NORMAL)
    plt.scatter(tempo, dados[:, Composito.NDVI_MEDIA_FLORESTA_REFERENCIA],\
        c="white", edgecolor="red", s=92, lw=2, alpha=0.8, label=u"Floresta")
    plt.scatter(tempo, dados[:, Composito.NDVI_MEDIA_MATO_REFERENCIA],\
        c="white", edgecolor="blue", s=92, lw=2, alpha=0.8, label=u"Mato")
    plt.scatter(tempo, referencia, c="green", s=imagens * diametro, alpha=0.5, label=u"Vegetação")
    serie_referencia.desenha(cor="orange", nome=u"Regressão")
    plt.legend(loc=8, fancybox=True, frameon=True, shadow=True, fontsize=FONTE_NORMAL)
    plt.show()
    serie_referencia.relatorio()

# Atualizar com o nome do ficheiro que se pretende utilizar
executa_calculo("dados/pedrogao.ndvi")
