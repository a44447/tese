# -*- coding: utf-8 -*-
"""
Modelo de cálculo de tempo de recuperação da vegetação usando decaimento exponencial

@author: Rui Reis
"""

import math
import pickle
import numpy as np
import matplotlib.pyplot as plt
from recveg import Utilidades, Composito
from recveg.calculo import DecaimentoExponencial

# ==========
# Constantes
# ==========
# Dimensão das fontes de texto
FONTE_NORMAL = 32
FONTE_PEQUENA = 24
ESPACO_LEGENDA = 8
# O limiar da normalidade será 10% da diferença máxima de DVI observada após o incêndio
LIMIAR = 0.10

def executa_calculo(nome_ficheiro):
    #pylint: disable=R0914
    """
    Executa o cálculo Modelo de cálculo de tempo de recuperação da
    vegetação usando decaimento exponencial
    """
    # Recupera os dados recolhidos no GEE, séries temporais de NDVI
    ficheiro = open(nome_ficheiro, "rb")
    modelo = pickle.load(ficheiro, encoding="latin1")
    dados = modelo["tabela"]

    # =================
    # Extração de dados
    # =================
    # Tempo
    tempo = dados[:, Composito.DATA_FIM].reshape(-1, 1)
    data_incendio = modelo["comum"]["data_incendio"]
    data_primeira_imagem = tempo[0]
    tempo = (tempo - data_primeira_imagem) / Utilidades.DIA
    # Racio para o diâmetro do ponto no gráfico
    imagens = dados[:, Composito.IMAGENS]
    diametro = float(364) / (float(max(imagens) - min(imagens)) + 1)
    # Diferencas de NDVI
    diferenca = np.array(dados[:, Composito.NDVI_MEDIA_VEGETACAO_ALVO] -\
        dados[:, Composito.NDVI_MEDIA_VEGETACAO_REFERENCIA]).reshape(-1, 1)
    # Regressão usando o decaimento exponencial
    diferenca_estimada = DecaimentoExponencial(tempo, diferenca)
    # Apresenta as estatísticas
    coeficiente_b = round(diferenca_estimada.coeficientes[0], 4)
    coeficiente_a = np.round(diferenca[0], 4)
    tempo_estimado = round(math.log(LIMIAR) / coeficiente_b, 0)
    data_estimada = data_primeira_imagem + tempo_estimado * Utilidades.DIA
    diferenca_estimada.relatorio()
    print("%-40s%s" % (u"Data do incêndio", Utilidades.formata_data(data_incendio)))
    print("%-40s%s" % (u"Data da primeiro imagem", Utilidades.formata_data(data_primeira_imagem)))
    print("%-40s%10.5f" % ("a=", coeficiente_a))
    print("%-40s%10.5f" % ("b=", coeficiente_b))
    print("%-40s%10.5f" % ("t=", tempo_estimado))
    print("%-40s%s" % (u"Data estimada de recuperação", Utilidades.formata_data(data_estimada)))

    # =======
    # Gráfico
    # =======
    # Prepara
    #pylint: disable=W0612
    figura, eixo_diferenca = plt.subplots(figsize=(16, 10))
    eixo_percentagem = eixo_diferenca.twinx()
    plt.style.use("seaborn-darkgrid")
    eixo_diferenca.set_xlabel(u"Dias após o primeira imagem válida (t)", fontsize=FONTE_NORMAL)
    eixo_diferenca.set_ylabel(u"Percentagem", fontsize=FONTE_NORMAL, labelpad=ESPACO_LEGENDA)
    eixo_percentagem.set_ylabel(u"Diferença", fontsize=FONTE_NORMAL, labelpad=ESPACO_LEGENDA)
    eixo_diferenca.tick_params(axis="x", labelsize=FONTE_PEQUENA)
    eixo_diferenca.tick_params(axis="y", labelsize=FONTE_PEQUENA)
    eixo_percentagem.tick_params(axis="y", labelsize=FONTE_PEQUENA)

    plt.scatter(tempo, diferenca, c="green", s=imagens * diametro, alpha=0.5, label=u"${y(t)}$")
    #  Ajusta a escala da percentagem
    diferencac_minima = (eixo_percentagem.get_ylim()[0] / coeficiente_a) * 100
    eixo_diferenca.set_ylim(diferencac_minima, 0)
    diferenca_estimada.desenha(cor="orange", nome=u"${\\hat y(t)}$")
    plt.legend(loc=2, fancybox=True, frameon=True, shadow=True, fontsize=FONTE_NORMAL)
    plt.show()

# Atualizar com o nome do ficheiro que se pretende utilizar
executa_calculo("dados/pedrogao-atual.ndvi")
