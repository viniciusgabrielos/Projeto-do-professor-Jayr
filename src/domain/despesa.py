from src.domain.lancamento import Lancamento
from src.domain.categoria import TipoCategoria, Categoria


class Despesa(Lancamento):
    """
    Representa uma SAÍDA de dinheiro no controle financeiro.

    Herda as características básicas de Lancamento e permite
    registrar valores gastados pelo usuário, como alimentação no mercado.

    Suas informações são utilizadas no cálculo do saldo
    financeiro e no acompanhamento do orçamento mensal.
    """

    def __init__(
        self,
        valor,
        categoria,
        data,
        descricao,
        forma_de_pagamento,
        id=None
    ):
        if not isinstance(categoria, Categoria):
            raise ValueError("O lançamento deve possuir uma categoria")

        if categoria.tipo != TipoCategoria.DESPESA:
            raise ValueError(
                "Uma despesa precisa de uma categoria do tipo DESPESA"
            )

        super().__init__(
            valor,
            categoria,
            data,
            descricao,
            forma_de_pagamento,
            id
        )