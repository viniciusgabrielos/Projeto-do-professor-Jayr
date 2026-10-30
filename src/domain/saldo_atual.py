class SaldoAtual:
    """
    Representa a consulta do saldo financeiro de um determinado dia.

    Utiliza as receitas e despesas registradas na data
    correspondente para calcular o resultado financeiro diário.

    Permite verificar a movimentação do dia sem precisar
    armazenar um saldo fixo, pois o valor pode ser obtido
    a partir dos lançamentos associados à data.
    """

    
    def __init__(self, receita_repositorio, despesa_repositorio):
        self.receita_repositorio = receita_repositorio
        self.despesa_repositorio = despesa_repositorio

    def calcular_saldo(self):
        receitas = self.receita_repositorio.listar_receitas()
        despesas = self.despesa_repositorio.listar_despesas()

        total_receitas = 0
        total_despesas = 0

        for dados in receitas.values():
            total_receitas += dados["valor"]

        for dados in despesas.values():
            total_despesas += dados["valor"]

        return total_receitas - total_despesas
