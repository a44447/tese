# -*- coding: utf-8 -*-
"""
Séries harmónicas da área ardida e da área de referência

@author: Rui Reis
"""

import pickle
import numpy as np
from recveg import Utilidades, Composito
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
    produz o gráfico
    """
    ficheiro = open(nome_ficheiro, "rb")
    modelo = pickle.load(ficheiro, encoding='latin1')
    dados = modelo["tabela"]

    # O tempo é relativo à primeira imagem válida
    tempo = dados[:, Composito.DATA_FIM].reshape(-1, 1)
    tempo = (tempo - tempo[0]) / Utilidades.DIA
    alvo = np.array(dados[:, Composito.NDVI_MEDIA_VEGETACAO_ALVO]).reshape(-1, 1)
    referencia = np.array(dados[:, Composito.NDVI_MEDIA_VEGETACAO_REFERENCIA]).reshape(-1, 1)

    # Estima as séries
    serie_referencia = SerieHarmonica(tempo, referencia, ciclo=365)
    # A série alvo só é calculada após a de referencia para simplificar a apresentação
    # do gráfico
    serie_alvo = SerieHarmonica(tempo, alvo, referencia=serie_referencia, ciclo=365)

    serie_alvo.relatorio()
    serie_alvo.grafico(titulo=None, cor_referencia="red", cor_alvo="blue")

# Atualizar com o nome do ficheiro que se pretende utilizar
executa_calculo("dados/pedrogao.ndvi")
