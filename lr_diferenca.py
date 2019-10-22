# -*- coding: utf-8 -*-
"""
Gráfico das diferenças de NDVI

@author: Rui Reis
"""

import pickle
import numpy as np
import matplotlib.pyplot as plt
from recveg import Composito, Utilidades

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
    Algoritmo de produção do gráfico das diferenças de NDVI em função
    da diferença máxima observada
    """
    ficheiro = open(nome_ficheiro, "rb")
    modelo = pickle.load(ficheiro, encoding='latin1')
    dados = modelo["tabela"]

    tempo = dados[:, Composito.DATA_FIM].reshape(-1, 1)
    tempo = (tempo - tempo[0]) / Utilidades.DIA
    diametro = float(364) / \
        (float(max(dados[:, Composito.IMAGENS]) - \
               min(dados[:, Composito.IMAGENS]))+1)
    diferenca = np.array(\
        dados[:, Composito.NDVI_MEDIA_VEGETACAO_ALVO] -\
        dados[:, Composito.NDVI_MEDIA_VEGETACAO_REFERENCIA])\
        .reshape(-1, 1)
    diferenca_maxima = diferenca[0]

    plt.figure(1, figsize=(16, 10))
    plt.style.use("seaborn-darkgrid")
    plt.xlabel(u"Dias após a primeira imagem (t)", fontsize=FONTE_NORMAL)
    plt.ylabel(u"$\\frac{NDVI(t)-NDVI^*(t)}{a}$", fontsize=FONTE_NORMAL)
    plt.xticks(fontsize=FONTE_PEQUENA)
    plt.yticks(fontsize=FONTE_PEQUENA)

    plt.scatter(tempo,\
                diferenca/diferenca_maxima,\
                c="green",\
                s=dados[:, Composito.IMAGENS] * diametro,\
                alpha=0.5,\
                label=u"Vegetação")
    plt.show()

# Atualizar com o nome do ficheiro que se pretende utilizar
executa_calculo("dados/pedrogao.ndvi")
