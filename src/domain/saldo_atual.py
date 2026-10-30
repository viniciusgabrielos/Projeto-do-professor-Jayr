class SaldoAtual:
    """
    Representa a consulta do saldo financeiro da atualidade, juntando todos os lancamento 
    do indivíduo, até o dia que ele queira consultar, ou seja, seu saldo disponível.
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
