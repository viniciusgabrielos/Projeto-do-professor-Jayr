from src.domain.lancamento import Lancamento
from src.domain.categoria import TipoCategoria
from src.domain.categoria import Categoria

class Despesa(Lancamento):
    """
    Representa uma saída de dinheiro no controle financeiro.

    Herda as características básicas de Lancamento e permite
    registrar gastos realizados pelo usuário, como alimentação,
    transporte, moradia e lazer.

    Participa do cálculo dos gastos diários e mensais, podendo
    gerar alertas quando ultrapassa limites financeiros
    estabelecidos pelo sistema.
    """
   
    def __init__(
        self, valor, categoria, data, descricao, forma_de_pagamento, id = None
    ):
        if not isinstance(categoria, Categoria):
            raise ValueError("O lançamento deve possuir uma categoria")

        if categoria.tipo != TipoCategoria.DESPESA:
            raise ValueError("Uma despesa precisa de uma categoria do tipo DESPESA"
    )

        super().__init__(valor, categoria, data, descricao, forma_de_pagamento, id
)


    