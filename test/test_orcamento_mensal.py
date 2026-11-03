
from src.domain.orcamento_mensal import OrcamentoMensal


# Simula o repositório de receitas para os testes.
class ReceitaRepositorioFake:
    def __init__(self, receitas):
        self.receitas = receitas

    # Retorna as receitas simuladas.
    def listar_receitas(self):
        return self.receitas


# Simula o repositório de despesas para os testes.
class DespesaRepositorioFake:
    def __init__(self, despesas):
        self.despesas = despesas

    # Retorna as despesas simuladas.
    def listar_despesas(self):
        return self.despesas


# Cria um orçamento mensal com lançamentos simulados.
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

    # Injeta os repositórios simulados no orçamento.
    receita_repositorio = ReceitaRepositorioFake(receitas)
    despesa_repositorio = DespesaRepositorioFake(despesas)

    return OrcamentoMensal(
        mes=mes,
        ano=ano,
        receita_repositorio=receita_repositorio,
        despesa_repositorio=despesa_repositorio,
        receita_prevista=3000.0
    )


# Verifica o total de receitas do mês de outubro.
def test_calcular_receitas_outubro():
    orcamento = criar_orcamento()
    assert orcamento.calcular_receitas() == 4550.0


# Verifica o total de despesas do mês de outubro.
def test_calcular_despesas_outubro():
    orcamento = criar_orcamento()
    assert orcamento.calcular_despesas() == 2230.0


# Verifica o saldo mensal após receitas e despesas.
def test_calcular_saldo_outubro():
    orcamento = criar_orcamento()
    assert orcamento.calcular_saldo() == 2320.0


# Verifica se o orçamento identifica corretamente a ausência de déficit.
def test_verificar_deficit_outubro():
    orcamento = criar_orcamento()
    assert orcamento.verificar_deficit() is False


# Verifica se lançamentos de outros meses são desconsiderados.
def test_ignorar_lancamentos_de_outros_meses():
    orcamento = criar_orcamento(mes=9, ano=2026)

    assert orcamento.calcular_receitas() == 450.0
    assert orcamento.calcular_despesas() == 90.0
