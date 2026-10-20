from src.domain.lancamento import Lancamento

class Receita(Lancamento):
    """
    Representa uma entrada de dinheiro no controle financeiro.

    Herda as características básicas de Lancamento e permite
    registrar valores recebidos pelo usuário, como salário,
    trabalhos extras ou outras fontes de renda.

    Suas informações são utilizadas no cálculo do saldo
    financeiro e no acompanhamento do orçamento mensal.
    """
    
    
    def __init__(
        self, valor, categoria, data, descricao, forma_de_pagamento
    ):
        super().__init__(
            valor, categoria, data, descricao, forma_de_pagamento
        )
    
    
    
    def cadastrarReceita(self):
        pass

    def editarReceita(self):
        pass