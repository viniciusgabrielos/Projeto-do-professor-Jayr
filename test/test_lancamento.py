import pytest
from datetime import date

from src.domain.categoria import Categoria, TipoCategoria
from src.domain.lancamento import Lancamento


def test_criar_lancamento_valido():
    categoria = Categoria(
        nome="Alimentação",
        tipo=TipoCategoria.DESPESA,
        descricao="Gastos com mercado",
        limite=800
    )

    lancamento = Lancamento(
        valor=50.0,
        categoria=categoria,
        data=date(2026, 10, 20),
        descricao="Compra no mercado",
        forma_de_pagamento="PIX"
    )

    assert lancamento.valor == 50.0
    assert lancamento.categoria == categoria
    assert lancamento.data == date(2026, 10, 20)
    assert lancamento.descricao == "Compra no mercado"
    assert lancamento.forma_de_pagamento == "PIX"

def test_lancamento_rejeita_valor_invalido():
    categoria = Categoria(
        nome="Alimentação",
        tipo=TipoCategoria.DESPESA,
        descricao="Gastos com mercado",
        limite=800
    )

    with pytest.raises(ValueError, match="O valor deve ser maior que 0"):
        Lancamento(
            valor=0,
            categoria=categoria,
            data=date(2026, 10, 20),
            descricao="Compra no mercado",
            forma_de_pagamento="PIX"
        )