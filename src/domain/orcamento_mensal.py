class OrcamentoMensal:
    """
    Representa o planejamento financeiro de um determinado mês.

    Reúne as previsões de receitas e despesas e os lançamentos
    financeiros associados ao período.

    É responsável por fornecer os cálculos de receitas,
    despesas e saldo disponível, permitindo acompanhar
    a situação financeira mensal e identificar possíveis
    déficits no orçamento.
    """
   
    def __init__(self, mes, ano, receita_repositorio, despesa_repositorio):

        if type(mes) != int:
            raise ValueError("O mês deve ser um inteiro")

        if mes < 1 or mes > 12:
            raise ValueError("O mês deve estar entre 1 e 12")

        if type(ano) != int:
            raise ValueError("O ano deve ser um inteiro")

        if ano < 1900 or ano > 2100:
            raise ValueError("O ano deve estar entre 1900 e 2100")


        self.mes = mes
        self.ano = ano
        self.receita_repositorio = receita_repositorio
        self.despesa_repositorio = despesa_repositorio

    def calcular_receitas(self):
        """
        Calcula o total de receitas registradas no orçamento mensal.

        Retorna a soma dos valores das receitas cadastradas
        para o mês e ano especificados.
        """
        receitas = self.receita_repositorio.listar_receitas()
        total = 0
        for id_receita, dados in receitas.items():
            data = dados["data"]
            valor = dados["valor"]

            ano,mes,dia = data.split("-")

            ano_data = int(ano)
            mes_data = int(mes)

            if ano_data == self.ano and mes_data == self.mes:
                total += valor
        return total
    def calcular_despesas(self):
        """
        Calcula o total de despesas registradas no orçamento mensal.

        Retorna a soma dos valores das despesas cadastradas
        para o mês e ano especificados.
        """
        despesas = self.despesa_repositorio.listar_despesas()
        total = 0
        for id_despesa, dados in despesas.items():
            data = dados["data"]
            valor = dados["valor"]

            ano,mes,dia = data.split("-")

            ano_data = int(ano)
            mes_data = int(mes)

            if ano_data == self.ano and mes_data == self.mes:
                total += valor
        return total

    def calcular_saldo(self):
        saldo = self.calcular_receitas() - self.calcular_despesas()
        return saldo

    def verificar_deficit(self):
        return self.calcular_saldo()<0