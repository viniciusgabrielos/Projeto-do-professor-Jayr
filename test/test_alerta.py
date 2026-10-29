import json
from datetime import date
from src.domain.alerta import Alerta, TipoAlerta
from src.repositories.alerta_repository import Alerta_Repositorio
import pytest
from unittest.mock import Mock
from src.domain.regras_alertas import verificar_alerta_alto_valor



def test_criar_alerta_com_dados_validos():
    alerta = Alerta(
        tipo=TipoAlerta.ALTO_VALOR,
        mensagem="Despesa acima de R$ 500,00"
    )

    assert alerta.tipo == TipoAlerta.ALTO_VALOR
    assert alerta.mensagem == "Despesa acima de R$ 500,00"
    assert alerta.data == date.today()


def test_alerta_rejeita_tipo_invalido():
    with pytest.raises(ValueError):
        Alerta(
            tipo="alto_valor",
            mensagem="Despesa acima de R$ 500,00"
        )


def test_alerta_rejeita_mensagem_vazia():
    with pytest.raises(ValueError):
        Alerta(
            tipo=TipoAlerta.ALTO_VALOR,
            mensagem="   "
        )


def test_alerta_rejeita_data_invalida():
    with pytest.raises(ValueError):
        Alerta(
            tipo=TipoAlerta.ALTO_VALOR,
            mensagem="Despesa acima do limite",
            data="28/10/2026"
        )




def test_adicionar_alerta_salva_no_json(tmp_path):
    repositorio = Alerta_Repositorio()
    repositorio.caminho = tmp_path / "alertas.json"

    alerta = Alerta(
        tipo=TipoAlerta.ALTO_VALOR,
        mensagem="Despesa de alto valor",
        data=date(2026, 10, 29)
    )

    repositorio.adicionar_alerta(alerta)

    with repositorio.caminho.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    assert "1" in dados
    assert dados["1"]["tipo"] == "alto_valor"
    assert dados["1"]["mensagem"] == "Despesa de alto valor"
    assert dados["1"]["data"] == "2026-10-29"


def test_adicionar_varios_alertas_gera_ids_sequenciais(tmp_path):
    repositorio = Alerta_Repositorio()
    repositorio.caminho = tmp_path / "alertas.json"

    primeiro = Alerta(
        tipo=TipoAlerta.ALTO_VALOR,
        mensagem="Primeiro alerta"
    )
    segundo = Alerta(
        tipo=TipoAlerta.LIMITE_EXCEDIDO,
        mensagem="Segundo alerta"
    )

    repositorio.adicionar_alerta(primeiro)
    repositorio.adicionar_alerta(segundo)

    assert list(repositorio.listar_alertas().keys()) == ["1", "2"]


def test_listar_alertas_retorna_os_alertas_salvos(tmp_path):
    repositorio = Alerta_Repositorio()
    repositorio.caminho = tmp_path / "alertas.json"

    alerta = Alerta(
        tipo=TipoAlerta.DEFICIT_ORCAMENTARIO,
        mensagem="Orçamento mensal negativo"
    )

    repositorio.adicionar_alerta(alerta)
    alertas = repositorio.listar_alertas()

    assert len(alertas) == 1
    assert alertas["1"]["tipo"] == "deficit_orcamentario"





def test_despesa_abaixo_do_limite_nao_gera_alerta(monkeypatch):
    monkeypatch.setattr(
        "src.domain.regras_alertas.carregar_configuracoes",
        lambda: {"limite_alerta_alto_valor": 500.0}
    )

    despesa = Mock()
    despesa.valor = 400.0
    repositorio = Mock()

    resultado = verificar_alerta_alto_valor(despesa, repositorio)

    assert resultado is None
    repositorio.adicionar_alerta.assert_not_called()


def test_despesa_igual_ao_limite_gera_alerta(monkeypatch):
    monkeypatch.setattr(
        "src.domain.regras_alertas.carregar_configuracoes",
        lambda: {"limite_alerta_alto_valor": 500.0}
    )

    despesa = Mock()
    despesa.valor = 500.0
    repositorio = Mock()

    resultado = verificar_alerta_alto_valor(despesa, repositorio)

    assert resultado.tipo == TipoAlerta.ALTO_VALOR
    repositorio.adicionar_alerta.assert_called_once_with(resultado)


def test_despesa_acima_do_limite_gera_alerta(monkeypatch):
    monkeypatch.setattr(
        "src.domain.regras_alertas.carregar_configuracoes",
        lambda: {"limite_alerta_alto_valor": 500.0}
    )

    despesa = Mock()
    despesa.valor = 600.0
    repositorio = Mock()

    resultado = verificar_alerta_alto_valor(despesa, repositorio)

    assert resultado.tipo == TipoAlerta.ALTO_VALOR
    repositorio.adicionar_alerta.assert_called_once_with(resultado)
