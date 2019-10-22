# -*- coding: utf-8 -*-
"""
Avaliação dos últimos 150 dias

@author: Rui Reis
"""

import pickle
from recveg import Composito, Utilidades

def executa_calculo(nome_ficheiro):
    """
    Algoritmo de produção do gráfico das diferenças de NDVI em função
    da diferença máxima observada
    """
    ficheiro = open(nome_ficheiro, "rb")
    modelo = pickle.load(ficheiro, encoding='latin1')
    dados = modelo["tabela"]

    maximo = dados[0, Composito.NDVI_MEDIA_VEGETACAO_ALVO]-\
        dados[0, Composito.NDVI_MEDIA_VEGETACAO_REFERENCIA]
    tempo = dados[-10:, Composito.DATA_FIM]
    alvo = dados[-10:, Composito.NDVI_MEDIA_VEGETACAO_ALVO]
    referencia = dados[-10:, Composito.NDVI_MEDIA_VEGETACAO_REFERENCIA]
    diferenca = alvo-referencia
    
    for elemento in range(10):
        print("%s & %3.1f\\%% & %5.4f & %5.4f & %5.4f\\\\" % (Utilidades.formata_data(tempo[elemento]),\
            100 * diferenca[elemento] / maximo,\
            alvo[elemento],\
            referencia[elemento],\
            diferenca[elemento]))

# Atualizar com o nome do ficheiro que se pretende utilizar
executa_calculo("dados/pedrogao-atual.ndvi")
