# -*- coding: utf-8 -*-
"""
Série harmónica

@author: Rui Reis
"""
import math
import numpy as np
from sklearn.linear_model import LinearRegression
from .modelobase import ModeloBase

class SerieHarmonica(ModeloBase):
    """Modelo sazonal baseado numa série temporal harmónica"""
    def __init__(self, x, y, nivel_confianca=0.95, referencia=None, ciclo=365):
        #pylint: disable=R0913
        # Por omissão, o ciclo é anual assumindo que o tempo t está expresso
        # em dias
        self.__ciclo = ciclo
        super(SerieHarmonica, self).__init__(x, y, nivel_confianca, referencia)

    def _regressor(self, x, y, xs):
        # Construcção da série temporal harmónica
        x_sin = [math.sin(2 * w * math.pi / self.__ciclo) for w in xs]
        x_cos = [math.cos(2 * w * math.pi / self.__ciclo) for w in xs]
        serie = np.column_stack((xs, x_sin, x_cos))
        regressor = LinearRegression().fit(serie[:x.shape[0]], y)
        estimado = regressor.predict(serie)
        return (regressor.coef_, regressor.intercept_, x, y, estimado, xs)
