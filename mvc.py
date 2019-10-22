# -*- coding: utf-8 -*-
"""
Aplicação cliente que permite agregar, extrair e persistir os dados do GEE
para um qualquer evento de incêndio na base de dados do ICNF

@author: Rui Reis
"""
import ee
from recveg import Modelo, ModeloNotificacao, Utilidades, ZonasArdidas

ee.Initialize()

# Simplifica a geometria a segmentos de 100m
TOLERANCIA = 100
# A zona de referência será uma faixa de 300m à volta da zona ardida
DISTANCIA = 300
# O MVC será avaliado para intervalos de 10 dias
CICLO = 10
# Travão de segurança para o ciclo de avaliação (100 iterações)
TRAVAO = 100
# dentificadore únicos dos incêndios na base de dados do ICNF
PEDROGAO = "BL4171577"
LEIRIA = "BL4172371"
# Formato consola
FORMATO_STR = "%-16s:\t%s"
FORMATO_MTR = "%-16s:\t%6dm"
FORMATO_DEC = "%-16s:\t%6d"

def notificacoes(dados, estagio):
    """Recebe as notificações do modelo de avaliação"""
    if estagio == ModeloNotificacao.INICIO:
        print("  %s" % (Utilidades.formata_data(dados)))
    elif estagio == ModeloNotificacao.SUCESSO:
        data_inicio = Utilidades.formata_data_hora(dados.inicio)
        if dados.imagens > 1:
            data_fim = Utilidades.formata_data_hora(dados.fim)
            print(" %d imagens (%s->%s)" % (dados.imagens, data_inicio, data_fim))
        else:
            print(" %d imagem (%s)" % (dados.imagens, data_inicio))
    elif estagio == ModeloNotificacao.VAZIO:
        print(" vazio")
    return True

def avalia_local(local, ficheiro, recupera=False):
    """Avalia, extrai e persiste os dados para o local indicado"""
    # pylint: disable=W0703
    modelo = Modelo(local, TOLERANCIA, DISTANCIA, CICLO)
    modelo.inicializa()
    if recupera:
        print(u"\nA atualizar ficheiro existente")
        try:
            modelo.carrega(ficheiro)
        except Exception as erro:
            print(erro)
    else:
        print(u"\nA avaliar a área ardida")

    print(modelo.evento)
    print(u"Dados de satélite")
    print(FORMATO_MTR % ("Escala", (modelo.escala)))
    print(FORMATO_STR % ("Pri. imagem", Utilidades.formata_data(modelo.data_primeira_imagem)))
    modelo.alvo.avalia()
    modelo.alvo.imprime(u"\nDimensões da zona do incêndio")
    modelo.referencia.avalia()
    modelo.referencia.imprime(u"\nDimensões da zona de referência")
    print("\nCompósitos:")
    #try:
    modelo.avalia(maximo=TRAVAO, evento=notificacoes)
    #except Exception as erro:
        #print(erro)

    modelo.guarda(ficheiro, esmaga=True)
    return modelo

def histograma():
    print(u"Distribuição de eventos de incêndio por Distrito:")
    lista = ZonasArdidas().distritos()
    for distrito in lista.keys():
        print(FORMATO_DEC % (distrito, lista[distrito]))
        
histograma()
avalia_local(PEDROGAO, "pedrogao-6.ndvi", recupera=True)
