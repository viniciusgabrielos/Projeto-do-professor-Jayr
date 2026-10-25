import pytest
from datetime import date
from src.domain.categoria import Categoria, TipoCategoria
from src.domain.lancamento import Lancamento
from src.domain.receita import Receita
from src.domain.despesa import Despesa

def test_criar_receita_valida():
    categoria = Categoria(
        nome="Aulas",
        tipo=TipoCategoria.RECEITA,
        descricao="Recebimentos por aulas"
    )

    receita = Receita(
        valor=2000,
        categoria=categoria,
        data=date.today(),
        descricao="Aulas particulares",
        forma_de_pagamento="PIX"
    )

    assert isinstance(receita, Receita)
    assert isinstance(receita, Lancamento)
    assert receita.valor == 2000
    assert receita.categoria is categoria


def test_receita_rejeita_valor_invalido():
    categoria = Categoria(
        nome="Aulas",
        tipo=TipoCategoria.RECEITA,
        descricao="Recebimentos por aulas"
    )

    with pytest.raises(
        ValueError,
        match="O valor deve ser maior que 0"
    ):
        Receita(
            valor=-100,
            categoria=categoria,
            data=date.today(),
            descricao="Aulas particulares",
            forma_de_pagamento="PIX"
        )

def test_receita_rejeita_categoria_invalida():
    with pytest.raises(
        ValueError,
        match="O lançamento deve possuir uma categoria"
    ):
        Receita(
            valor=2000,
            categoria="Aulas",
            data=date.today(),
            descricao="Aulas particulares",
            forma_de_pagamento="PIX"
        )


def test_verifica_se_despesa_tem_categoria_despesa():
    categoria = Categoria(nome="Ifood", tipo=TipoCategoria.DESPESA,limite=500)
    despesa = Despesa(valor=100,categoria=categoria,data=date.today(),descricao="Compra de uma pizza",forma_de_pagamento="Débito")

    assert isinstance(despesa,Despesa)
    assert isinstance(despesa,Lancamento)

def test_rejeita_despesa_se_categoria_for_receita():
    with pytest.raises(ValueError, match="Uma despesa precisa de uma categoria do tipo DESPESA"):
        categoria = Categoria(nome="Salário",tipo=TipoCategoria.RECEITA)
        despesa = Despesa(valor=100,categoria=categoria,data=date.today(),descricao="Compra de uma pizza",forma_de_pagamento="Débito")

def test_receita_rejeita_categoria_despesa():
    categoria = Categoria(
        nome="Alimentação",
        tipo=TipoCategoria.DESPESA,
        limite=500
    )

    with pytest.raises(
        ValueError,
        match="Uma receita precisa de uma categoria do tipo RECEITA"
    ):
        receita = Receita(
            valor=100,
            categoria=categoria,
            data=date.today(),
            descricao="Salário",
            forma_de_pagamento="PIX"
        )