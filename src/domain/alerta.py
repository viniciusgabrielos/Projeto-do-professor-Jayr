from enum import Enum
from datetime import date


class TipoAlerta(Enum):
    ALTO_VALOR = "alto_valor"
    LIMITE_EXCEDIDO = "limite_excedido"
    DEFICIT_ORCAMENTARIO = "deficit_orcamentario"
    PREVISAO_RECEITA = "previsao_receita"
    META_ECONOMIA = "meta_economia"
class Alerta:
    """
    Classe responsável por representar e gerenciar os alertas gerados pelo sistema, armazenando informações como a data, o tipo e a mensagem do alerta, além de permitir seu registro e apresentação ao usuário.

    """
  

    def __init__(self, tipo, mensagem, data=None):
        self.tipo = tipo
        self.mensagem = mensagem
        self.data = data if data is not None else date.today()

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, tipo):
        if not isinstance(tipo,TipoAlerta):
            raise ValueError("O tipo do alerta deve ser um TipoAlerta Válido")

        self._tipo = tipo

    @property
    def mensagem(self):
        return self._mensagem

    @mensagem.setter
    def mensagem(self, mensagem):
        if not isinstance(mensagem, str) or not mensagem.strip():
            raise ValueError("A mensagem deve ser um texto não vazio")

        self._mensagem = mensagem.strip()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        if not isinstance(data, date):
            raise ValueError("A data do alerta deve ser uma data válida")

        self._data = data
        