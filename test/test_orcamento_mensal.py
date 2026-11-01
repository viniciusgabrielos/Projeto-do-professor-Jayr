
from src.domain.orcamento_mensal import OrcamentoMensal


class ReceitaRepositorioFake:
    def __init__(self, receitas):
        self.receitas = receitas

    def listar_receitas(self):
        return self.receitas


class DespesaRepositorioFake:
    def __init__(self, despesas):
        self.despesas = despesas

    def listar_despesas(self):
        return self.despesas


def criar_orcamento(mes=10, ano=2026):
    receitas = {
        "1": {"valor": 1000.0, "data": "2026-10-05"},
        "2": {"valor": 2000.0, "data": "2026-10-15"},
        "3": {"valor": 1550.0, "data": "2026-10-25"},
        "4": {"valor": 450.0, "data": "2026-09-12"},
    }

    despesas = {
        "1": {"valor": 1000.0, "data": "2026-10-08"},
        "2": {"valor": 1230.0, "data": "2026-10-20"},
        "3": {"valor": 90.0, "data": "2026-09-18"},
    }

    receita_repositorio = ReceitaRepositorioFake(receitas)
    despesa_repositorio = DespesaRepositorioFake(despesas)

    return OrcamentoMensal(
        mes=mes,
        ano=ano,
        receita_repositorio=receita_repositorio,
        despesa_repositorio=despesa_repositorio,
        receita_prevista=3000.0
    )


def test_calcular_receitas_outubro():
    orcamento = criar_orcamento()
    assert orcamento.calcular_receitas() == 4550.0


def test_calcular_despesas_outubro():
    orcamento = criar_orcamento()
    assert orcamento.calcular_despesas() == 2230.0


def test_calcular_saldo_outubro():
    orcamento = criar_orcamento()
    assert orcamento.calcular_saldo() == 2320.0


def test_verificar_deficit_outubro():
    orcamento = criar_orcamento()
    assert orcamento.verificar_deficit() is False


def test_ignorar_lancamentos_de_outros_meses():
    orcamento = criar_orcamento(mes=9, ano=2026)

    assert orcamento.calcular_receitas() == 450.0
    assert orcamento.calcular_despesas() == 90.0
