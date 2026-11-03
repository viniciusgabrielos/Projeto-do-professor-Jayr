
from unittest.mock import Mock

from src.domain.relatorio import Relatorio
from datetime import date
import src.domain.relatorio as modulo_relatorio
from datetime import date as DataOriginal


# Cria um relatório com repositórios simulados.
def criar_relatorio(despesas=None, receitas=None, categorias=None):
    categoria_repositorio = Mock()
    categoria_repositorio.listar.return_value = categorias or {}

    despesa_repositorio = Mock()
    despesa_repositorio.categoria_repositorio = categoria_repositorio
    despesa_repositorio.listar_despesas.return_value = despesas or {}

    receita_repositorio = Mock()
    receita_repositorio.listar_receitas.return_value = receitas or {}

    return Relatorio(receita_repositorio, despesa_repositorio)


# Verifica o agrupamento e a soma das despesas por categoria.
def test_calcular_despesas_por_categoria():
    categorias = {
        "1": {"nome": "Alimentação", "tipo": "DESPESA"},
        "2": {"nome": "Transporte", "tipo": "DESPESA"},
        "3": {"nome": "Salário", "tipo": "RECEITA"}
    }

    despesas = {
        "1": {"categoria_id": 1, "valor": 50},
        "2": {"categoria_id": 1, "valor": 30},
        "3": {"categoria_id": 2, "valor": 20},
        "4": {"categoria_id": 3, "valor": 1000}
    }

    relatorio = criar_relatorio(despesas=despesas, categorias=categorias)

    resultado = relatorio.calcular_despesas_por_categoria()

    assert resultado == {
        "Alimentação": 80,
        "Transporte": 20
    }


# Verifica o retorno vazio quando não existem despesas.
def test_calcular_despesas_por_categoria_sem_despesas():
    relatorio = criar_relatorio()

    resultado = relatorio.calcular_despesas_por_categoria()

    assert resultado == {}


# Verifica o cálculo percentual das despesas por categoria.
def test_calcular_percentual_por_categoria():
    categorias = {
        "1": {"nome": "Alimentação", "tipo": "DESPESA"},
        "2": {"nome": "Transporte", "tipo": "DESPESA"}
    }

    despesas = {
        "1": {"categoria_id": 1, "valor": 80},
        "2": {"categoria_id": 2, "valor": 20}
    }

    relatorio = criar_relatorio(despesas=despesas, categorias=categorias)

    resultado = relatorio.calcular_percentual_por_categoria()

    assert resultado == {
        "Alimentação": 80.0,
        "Transporte": 20.0
    }


# Verifica o retorno vazio quando não existem despesas para calcular percentuais.
def test_calcular_percentual_sem_despesas():
    relatorio = criar_relatorio()

    resultado = relatorio.calcular_percentual_por_categoria()

    assert resultado == {}


# Verifica a identificação do mês com menor gasto.
def test_identificar_mes_mais_economico():
    despesas = {
        "1": {"data": "2026-01-10", "valor": 500},
        "2": {"data": "2026-01-20", "valor": 300},
        "3": {"data": "2026-02-10", "valor": 200},
        "4": {"data": "2026-03-10", "valor": 600}
    }

    relatorio = criar_relatorio(despesas=despesas)

    resultado = relatorio.identificar_mes_mais_economico()

    assert resultado == {
        "mes": 2,
        "ano": 2026,
        "total_despesas": 200
    }


# Verifica o retorno None quando não existem despesas.
def test_identificar_mes_mais_economico_sem_despesas():
    relatorio = criar_relatorio()

    resultado = relatorio.identificar_mes_mais_economico()

    assert resultado is None


# Verifica se são retornados os três últimos meses.
def test_obter_ultimos_meses():
    relatorio = criar_relatorio()

    resultado = relatorio._obter_ultimos_meses()

    assert len(resultado) == 3
    assert resultado[-1][1] >= 1
    assert resultado[-1][1] <= 12


# Verifica a comparação de receitas e despesas dos últimos meses.
def test_comparar_ultimos_meses():
    relatorio = criar_relatorio()

    meses = relatorio._obter_ultimos_meses()
    receitas = {}
    despesas = {}

    # Gera lançamentos para cada mês retornado.
    for i, (ano, mes) in enumerate(meses, start=1):
        receitas[str(i)] = {
            "data": f"{ano}-{mes:02d}-10",
            "valor": 1000 * i
        }

        despesas[str(i)] = {
            "data": f"{ano}-{mes:02d}-15",
            "valor": 500 * i
        }

    relatorio = criar_relatorio(receitas=receitas, despesas=despesas)

    resultado = relatorio.comparar_ultimos_meses()

    assert len(resultado) == 3

    # Confirma a presença dos totais de receitas e despesas.
    for valores in resultado.values():
        assert "receitas" in valores
        assert "despesas" in valores


# Simula janeiro de 2027 para verificar a virada do ano.
def test_obter_ultimos_meses_na_virada_do_ano(monkeypatch):
    class DataFalsa:
        @staticmethod
        def today():
            return date(2027, 1, 15)

    # Substitui a data atual utilizada pelo módulo.
    monkeypatch.setattr(modulo_relatorio, "date", DataFalsa)

    relatorio = criar_relatorio()

    resultado = relatorio._obter_ultimos_meses()

    assert resultado == [
        (2026, 11),
        (2026, 12),
        (2027, 1)
    ]


# Verifica a comparação mensal atravessando a virada do ano.
def test_comparar_ultimos_meses_na_virada_do_ano(monkeypatch):
    class DataFalsa:
        @staticmethod
        def today():
            return DataOriginal(2027, 1, 15)

        @staticmethod
        def fromisoformat(data):
            return DataOriginal.fromisoformat(data)

    # Simula a data atual e mantém a conversão de datas original.
    monkeypatch.setattr(modulo_relatorio, "date", DataFalsa)

    receitas = {
        "1": {"data": "2026-11-10", "valor": 1000},
        "2": {"data": "2026-12-10", "valor": 2000},
        "3": {"data": "2027-01-10", "valor": 3000}
    }

    despesas = {
        "1": {"data": "2026-11-15", "valor": 400},
        "2": {"data": "2026-12-15", "valor": 800},
        "3": {"data": "2027-01-15", "valor": 1200}
    }

    relatorio = criar_relatorio(
        receitas=receitas,
        despesas=despesas
    )

    resultado = relatorio.comparar_ultimos_meses()

    # Confirma os totais e os períodos corretamente identificados.
    assert resultado == {
        "11/2026": {"receitas": 1000, "despesas": 400},
        "12/2026": {"receitas": 2000, "despesas": 800},
        "01/2027": {"receitas": 3000, "despesas": 1200}
    }
