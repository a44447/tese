# -*- coding: utf-8 -*-
"""
Modelo de regressão linear enriquecido

@author: Rui Reis
"""
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import t
from sklearn.linear_model import LinearRegression

class ModeloBase:
    """Modelo de regressão linear enriquecido"""
    MAX_ITER = 10

    def __init__(self, x, y, nc=0.95, referencia=None, expande=False):
        self.__nc = nc
        self.__referencia = referencia
        if expande:
            xs = self.__expande(x)
        else:
            xs = x
        self.__variaveis(self._regressor(x, y, xs))

    def __expande(self, x):
        """Expande o eixo X com base do passo médio"""
        origem = x[-1, 0]
        passo = np.mean(np.diff(x[:, 0]))
        xs = (np.arange(0, self.MAX_ITER) * passo + origem).reshape(-1, 1)
        return np.vstack((x, xs))

    def _regressor(self, x, y, xs):
        """
        Método protegido que implementa o regresso para um dado modelo,
        implementa a regressão linear base
        """
        raise RuntimeError(u"O regressor terá que ser definido")

    def __variaveis(self, regressor):
        """Complementa o modelo de regressão com algumas estatísticas relevantes"""
        m, b, x, y, ye, xs = regressor
        self.__coeficientes = m
        self.__origem = b
        self.__n = len(x[:, 0])
        self.__k = x.shape[1]
        self.__x = x
        self.__mx = np.mean(x, axis=0)
        self.__xn = [x[:, i] - self.__mx[i] for i in range(self.__k)]
        self.__xs = xs
        self.__y = y
        self.__my = np.mean(y)
        self.__sy = np.var(y)
        self.__yn = y - self.__my
        self.__ye = ye
        self.__yr = y - self.__ye[:self.__n]
        self.__cr = t.interval(self.__nc, self.__n - self.__k - 1)[1]
        self.__sqy_res = sum(self.__yr ** 2)
        self.__sqx_tot = np.array([sum((x[:, i]-self.__mx[i]) ** 2) for i in range(self.__k)])
        self.__sqy_tot = sum((self.__y - self.__my) ** 2)
        self.__ep_est = math.sqrt(self.__sqy_res / (self.__n - self.__k - 1))
        self.__ic = np.array([[self.__cr * self.__ep_est * math.sqrt(1 / float(self.__n) + (o - self.__mx[i]) ** 2 / self.__sqx_tot[i]) for o in xs[:, i]] for i in range(self.__k)])
        self.__r2 = 1 - (self.__sqy_res / self.__sqy_tot)
        self.__r2_ajustado = 1 - (1 - self.__r2) * (self.__n - 1) / (self.__n - self.__k - 1)

    @property
    def coeficientes(self):
        """Coeficientes"""
        return self.__coeficientes

    @property
    def origem(self):
        """Valor na origem"""
        return self.__origem

    @property
    def n(self):
        """Número de observações"""
        return self.__n

    @property
    def graus_liberdade(self):
        """Número de graus de liberdade"""
        return self.__k

    @property
    def nivel_critico(self):
        """Nível crítico para cálculo dos intervalos de confiança"""
        return self.__cr

    @property
    def soma_quadrado_residuo_y(self):
        """Soma do quadrado do resíduo"""
        return self.__sqy_res

    @property
    def soma_quadrado_total_y(self):
        """Soma do quadrado total (observações normalizadas) das observações de NDVI"""
        return self.__sqy_tot

    @property
    def soma_quadrado_total_x(self):
        """Soma do quadrado total (datas normalizadas) da data das observações de NDVI"""
        return self.__sqx_tot

    @property
    def erro_padrao(self):
        """Erro padrão da estimativa"""
        return self.__ep_est

    @property
    def intervalo_confianca(self):
        """Intervalo de confiança"""
        return self.__ic

    @property
    def coeficiente_determinacao(self):
        """Coeficiente de determinção (R2)"""
        return self.__r2

    @property
    def coeficiente_determinacao_ajustado(self):
        """Coeficiente de determinção ajustado (R2 ajustado)"""
        return self.__r2_ajustado

    @property
    def intervalo_inferior(self):
        """Intervalo de confiança inferior"""
        return self.__ye[:, 0]-self.__ic[0]

    @property
    def intervalo_superior(self):
        """Intervalo de confiança superior"""
        return self.__ye[:, 0]+self.__ic[0]

    @property
    def x(self):
        """Valores de X, momentos das observações"""
        return self.__x

    @property
    def x_normalizado(self):
        """Valores de X normalizados"""
        return self.__xn

    @property
    def x_estimado(self):
        """Expansão do eixo dos X, usando a média das variações observadas"""
        return self.__xs

    @property
    def y(self):
        """Observações de NDVI"""
        return self.__y

    @property
    def estimado(self):
        """Estimativa de NDVI"""
        return self.__ye

    def relatorio(self, titulo=None):
        """Imprime um resumo das estatísticas da regressão"""
        MASCARA_INT = "%-40s%10d"
        MASCARA_FLT = "%-40s%10.5f"
        MASCARA_EXP = "%-40s%10.1E"

        if titulo is None:
            print(u"Estatísticas:")
        else:
            print(titulo)
        print(MASCARA_INT % ("n", self.__n))
        print(MASCARA_INT % ("Graus liberdade", self.__k))
        print(MASCARA_FLT % (u"Nível crítico", self.__cr))
        print(MASCARA_FLT % (u"Média Y", self.__my))
        print(MASCARA_FLT % (u"Variância Y", self.__sy))
        print(MASCARA_FLT % (u"S.Q. resíduo Y", self.__sqy_res))
        print(MASCARA_FLT % (u"S.Q. resíduo Y", self.__sqy_res))
        print(MASCARA_FLT % (u"S.Q. total Y", self.__sqy_tot))
        print(MASCARA_EXP % (u"S.Q. total X", self.__sqx_tot[0]))
        print(MASCARA_FLT % (u"Erro padrão est.", self.__ep_est))
        print(MASCARA_FLT % (u"C. determinação (R2).", self.__r2))
        print(MASCARA_FLT % (u"C. det. ajustado (R2 ajust.).", self.__r2_ajustado))

    def desenha(self, destino=plt, cor="blue", intervalo=True, qualidade=100, nome=None):
        """Produz um gráfico com as observações e estimativa com evidência do intervalo de confiança"""
        destino.scatter(self.__x[:, 0], self.__y, c="white", edgecolors=cor, linewidth=2, alpha=0.5, s=qualidade)
        destino.plot(self.__xs[:, 0], self.__ye, color=cor, linewidth=3, label=nome)
        if intervalo:
            destino.plot(self.__xs[:, 0], self.intervalo_inferior, color=cor, linewidth=1)
            destino.plot(self.__xs[:, 0], self.intervalo_superior, color=cor, linewidth=1)
            destino.fill_between(self.__xs[:, 0], self.intervalo_inferior,\
                self.intervalo_superior, color=cor, alpha=0.3, interpolate=True)

    def grafico(self, datas=None, titulo=None, cor_alvo="blue", cor_referencia="red", tamanho=(16, 10), destino=plt, qualidade=100):
        """Produz o gráfico da regressão"""
        # Dimensão das fontes de texto
        FONTE_NORMAL = 32
        FONTE_PEQUENA = 24
        destino.figure(figsize=tamanho)
        destino.style.use("seaborn-darkgrid")
        destino.xlabel("Dias após o primeira imagem válida(t)", fontsize=FONTE_NORMAL)
        destino.ylabel("NDVI", fontsize=FONTE_NORMAL)
        destino.xticks(fontsize=FONTE_PEQUENA)
        destino.yticks(fontsize=FONTE_PEQUENA)
        self.desenha(cor=cor_alvo, qualidade=qualidade)
        if self.__referencia is not None:
            self.__referencia.desenha(cor=cor_referencia, qualidade=qualidade)
        if datas is not None:
            intervalo = np.arange(0, len(self.__xs[:, 0]), 10)
            destino.xticks(self.__xs[intervalo], datas[intervalo, 0])
        if titulo is not None:
            destino.title(titulo, fontsize=FONTE_NORMAL)
        destino.show()
