
from src.domain.orcamento_mensal import OrcamentoMensal
from src.repositories.receita_repository import Receita_Repositorio
from src.repositories.despesa_repository import Despesa_Repositorio


def criar_orcamento(mes=10, ano=2026):
    return OrcamentoMensal(
        mes=mes,
        ano=ano,
        receita_repositorio=Receita_Repositorio(),
        despesa_repositorio=Despesa_Repositorio(),
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
