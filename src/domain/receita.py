
from src.domain.lancamento import Lancamento
from src.domain.categoria import TipoCategoria, Categoria


class Receita(Lancamento):
    """
    Representa uma entrada de dinheiro no controle financeiro.
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
        # Valida a categoria do lançamento
        if not isinstance(categoria, Categoria):
            raise ValueError("O lançamento deve possuir uma categoria")

        # Exige uma categoria de receita
        if categoria.tipo != TipoCategoria.RECEITA:
            raise ValueError("Uma receita precisa de uma categoria do tipo RECEITA")

        # Inicializa os atributos herdados
        super().__init__(
            valor,
            categoria,
            data,
            descricao,
            forma_de_pagamento,
            id
        )
