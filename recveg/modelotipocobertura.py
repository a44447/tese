# -*- coding: utf-8 -*-
"""
Modelo de um tipo de cobertura

@author: Rui Reis
"""

class ModeloTipoCobertura:
    """Classe que encapsula a funcionalidade de um tipo de cobertura"""
    
    def __init__(self, imagem, dimensao=0):
        self.__imagem = imagem
        self.__dimensao = dimensao

    @property
    def imagem(self):
        """Imagem da cobertura"""
        return self.__imagem

    @property
    def dimensao(self):
        """Dimensão, em pontos, da imagem"""
        return self.__dimensao
