from src.domain.lancamento import Lancamento
from src.domain.categoria import TipoCategoria, Categoria

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
        self, valor, categoria, data, descricao, forma_de_pagamento, id = None
    ):
        if not isinstance(categoria, Categoria):
            raise ValueError("O lançamento deve possuir uma categoria")

        if categoria.tipo != TipoCategoria.RECEITA:
            raise ValueError("Uma receita precisa de uma categoria do tipo RECEITA")
        super().__init__(
            valor, categoria, data, descricao, forma_de_pagamento, id
        )
    
    
    
    