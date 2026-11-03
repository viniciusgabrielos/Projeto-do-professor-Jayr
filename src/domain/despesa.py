
from src.domain.lancamento import Lancamento
from src.domain.categoria import TipoCategoria, Categoria


class Despesa(Lancamento):
    """
    Representa uma saída de dinheiro no controle financeiro.
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

        # Exige uma categoria de despesa
        if categoria.tipo != TipoCategoria.DESPESA:
            raise ValueError(
                "Uma despesa precisa de uma categoria do tipo DESPESA"
            )

        # Inicializa os atributos herdados
        super().__init__(
            valor,
            categoria,
            data,
            descricao,
            forma_de_pagamento,
            id
        )
