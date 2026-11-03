
class SaldoAtual:
    """
    Representa a consulta do saldo financeiro acumulado.
    """

    def __init__(self, receita_repositorio, despesa_repositorio):
        # Inicializa os repositórios financeiros
        self.receita_repositorio = receita_repositorio
        self.despesa_repositorio = despesa_repositorio

    def calcular_saldo(self):
        # Recupera receitas e despesas cadastradas
        receitas = self.receita_repositorio.listar_receitas()
        despesas = self.despesa_repositorio.listar_despesas()

        total_receitas = 0
        total_despesas = 0

        # Soma todas as receitas
        for dados in receitas.values():
            total_receitas += dados["valor"]

        # Soma todas as despesas
        for dados in despesas.values():
            total_despesas += dados["valor"]

        # Retorna receitas menos despesas
        return total_receitas - total_despesas
