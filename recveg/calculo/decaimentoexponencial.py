# -*- coding: utf-8 -*-
"""
Modelo de decaimento exponencial

@author: Rui Reis
"""
import math
import numpy as np
from sklearn.linear_model import LinearRegression
from .modelobase import ModeloBase

class DecaimentoExponencial(ModeloBase):
    """Modelo de decaimento exponencial"""
    def __init__(self, x, y, nivel_confianca=0.95, referencia=None):
        super(DecaimentoExponencial, self).__init__(x, y, nivel_confianca, referencia)

    def _regressor(self, x, y, xs):
        maximo = y[0]
        diferenca_relativa = [math.log(valor / maximo) for valor in y]
        regressor = LinearRegression(fit_intercept=False).fit(x, diferenca_relativa)
        estimativa = regressor.predict(xs)
        diferenca_estimada = np.array([maximo * math.exp(w) for w in estimativa])
        return (regressor.coef_, regressor.intercept_, x, y, diferenca_estimada, xs)
