# -*- coding: utf-8 -*-
"""
Avaliação dos últimos 150 dias

@author: Rui Reis
"""

import pickle
import numpy as np
import matplotlib.pyplot as plt
from recveg import Composito, Utilidades

def executa_calculo(nome_ficheiro):
    """
    Algoritmo de produção do gráfico das diferenças de NDVI em função
    da diferença máxima observada
    """
    ficheiro = open(nome_ficheiro, "rb")
    modelo = pickle.load(ficheiro, encoding='latin1')
    dados = modelo["tabela"]

    tempo = dados[:-10, Composito.DATA_FIM]
    alvo = dados[:-10, Composito.NDVI_MEDIA_VEGETACAO_ALVO]
    referencia = dados[:-10, Composito.NDVI_MEDIA_VEGETACAO_ALVO]
    diferenca = alvo-referencia
    
    for elemento in tempo:
        print(Utilidades.formata_data(elemento))

# Atualizar com o nome do ficheiro que se pretende utilizar
executa_calculo("dados/pedrogao-5.ndvi")
