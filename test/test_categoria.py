
import pytest

from src.domain.categoria import Categoria, TipoCategoria
from src.repositories.categoria_repository import Categoria_Repositorio


# Cria um repositório isolado para os testes.
def criar_repositorio(tmp_path):
    repositorio = Categoria_Repositorio()
    repositorio.caminho = tmp_path / "categorias.json"
    repositorio.categorias = {}
    repositorio.salvar()
    return repositorio


# Verifica o cadastro de uma categoria e sua identificação.
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


# Verifica se categorias com mesmo nome e tipo são rejeitadas.
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


# Verifica se categorias com mesmo nome e tipos diferentes são permitidas.
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


# Verifica a edição do nome de uma categoria cadastrada.
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


# Verifica se a edição de categoria inexistente gera erro.
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


# Verifica o tamanho do nome retornado pela categoria.
def test_len_categoria():
    categoria = Categoria(
        nome="Alimentação",
        tipo=TipoCategoria.DESPESA,
        limite=500
    )

    assert len(categoria) == 11


# Verifica a busca de trechos do nome sem diferenciar maiúsculas.
def test_contains_categoria():
    categoria = Categoria(
        nome="Alimentação",
        tipo=TipoCategoria.DESPESA,
        limite=500
    )

    assert "alim" in categoria
    assert "ALIMENTAÇÃO" in categoria
    assert "transporte" not in categoria
