# -*- coding: utf-8 -*-
"""
Classe com métodos de utlidades

@author: Rui Reis
"""
from datetime import datetime

class Utilidades:
    """Classe que encapsula um conjunto de métodos utilitários"""
    # Dia em milisegundos
    DIA = 24*60*60*1000

    @classmethod
    def agora(cls):
        """A data e hora atuais como um timestap de unix em milisegundos"""
        return datetime.now().timestamp() * 1e3

    @classmethod
    def dia_seguinte(cls, data):
        """Dia seguinte à data indicada como um timestamp de unix em milisegundos"""
        return cls.dia_apos(data, 1)

    @classmethod
    def dia_apos(cls, data, dias):
        """Dia correspondete à data indicada acrescida de um dado número de dias"""
        return data + cls.DIA * dias

    @classmethod
    def apenas_data(cls, data):
        """Eliminar do timestamp de unix em milisegundos a hora do dia"""
        return int(data / cls.DIA) * cls.DIA

    @classmethod
    def formata_data(cls, data, formato="%d-%m-%Y"):
        """Formata umtimestamp unix em milisegundos"""
        return datetime.fromtimestamp(data/ 1e3).strftime(formato)

    @classmethod
    def formata_data_hora(cls, data):
        """Formata umtimestamp unix em milisegundos"""
        return cls.formata_data(data, "%d-%m-%Y, %H:%M:%S")
    