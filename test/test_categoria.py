import pytest

from src.domain.categoria import Categoria, TipoCategoria
from src.repositories.categoria_repository import Categoria_Repositorio


def criar_repositorio(tmp_path):
    repositorio = Categoria_Repositorio()
    repositorio.caminho = tmp_path / "categorias.json"
    repositorio.categorias = {}
    repositorio.salvar()
    return repositorio


def test_adicionar_categoria(tmp_path):
    repositorio = criar_repositorio(tmp_path)

    categoria = Categoria(
        nome="Alimentação",
        tipo=TipoCategoria.DESPESA,
        descricao="Gastos com mercado",
        limite=800
    )

    repositorio.adicionar(categoria)

    assert categoria.id == 1
    assert "1" in repositorio.categorias
    assert repositorio.categorias["1"]["nome"] == "Alimentação"

def test_impedir_categoria_duplicada(tmp_path):
    repositorio = criar_repositorio(tmp_path)

    categoria1 = Categoria(
        nome="Alimentação",
        tipo=TipoCategoria.DESPESA,
        descricao="Gastos com mercado",
        limite=800
    )

    categoria2 = Categoria(
        nome="Alimentação",
        tipo=TipoCategoria.DESPESA,
        descricao="Compras de supermercado",
        limite=1000
    )

    repositorio.adicionar(categoria1)

    with pytest.raises(
    ValueError,
    match="Já existe uma categoria com esse nome e tipo"
):
        repositorio.adicionar(categoria2)

def test_permitir_mesmo_nome_tipo_diferente(tmp_path):
    repositorio = criar_repositorio(tmp_path)

    categoria_despesa = Categoria(
        nome="Alimentação",
        tipo=TipoCategoria.DESPESA,
        descricao="Gastos com mercado",
        limite=800
    )

    categoria_receita = Categoria(
        nome="Alimentação",
        tipo=TipoCategoria.RECEITA,
        descricao="Receitas relacionadas à alimentação"
    )

    repositorio.adicionar(categoria_despesa)
    repositorio.adicionar(categoria_receita)

    assert len(repositorio.categorias) == 2
    assert categoria_despesa.id != categoria_receita.id

def test_editar_categoria(tmp_path):
    repositorio = criar_repositorio(tmp_path)

    categoria = Categoria(
        nome="Alimentação",
        tipo=TipoCategoria.DESPESA,
        descricao="Gastos com mercado",
        limite=800
    )

    repositorio.adicionar(categoria)

    repositorio.editar(
        categoria.id,
        {"nome": "Supermercado"}
    )

    assert repositorio.categorias["1"]["nome"] == "Supermercado"

def test_editar_categoria_inexistente(tmp_path):
    repositorio = criar_repositorio(tmp_path)

    with pytest.raises(
    ValueError,
    match="Categoria não encontrada"
):
        repositorio.editar(
        99,
        {"nome": "Supermercado"}
        )