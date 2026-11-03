
from src.domain.settings import carregar_configuracoes


class OrcamentoMensal:
    """
    Representa o planejamento financeiro de um determinado mês.
    """

    def __init__(
        self,
        mes,
        ano,
        receita_repositorio,
        despesa_repositorio,
        receita_prevista
    ):
        # Valida o mês
        if type(mes) != int:
            raise ValueError("O mês deve ser um inteiro")

        if mes < 1 or mes > 12:
            raise ValueError("O mês deve estar entre 1 e 12")

        # Valida o ano
        if type(ano) != int:
            raise ValueError("O ano deve ser um inteiro")

        if ano < 1900 or ano > 2100:
            raise ValueError("O ano deve estar entre 1900 e 2100")

        # Inicializa o orçamento mensal
        self.mes = mes
        self.ano = ano
        self.receita_repositorio = receita_repositorio
        self.despesa_repositorio = despesa_repositorio
        self.receita_prevista = receita_prevista

    def calcular_receitas(self):
        """
        Soma as receitas do mês e ano especificados.
        """
        receitas = self.receita_repositorio.listar_receitas()
        total = 0

        # Percorre as receitas cadastradas
        for id_receita, dados in receitas.items():
            data = dados["data"]
            valor = dados["valor"]

            # Separa ano, mês e dia da data
            ano, mes, dia = data.split("-")

            ano_data = int(ano)
            mes_data = int(mes)

            # Soma receitas do período selecionado
            if ano_data == self.ano and mes_data == self.mes:
                total += valor

        return total

    def calcular_despesas(self):
        """
        Soma as despesas do mês e ano especificados.
        """
        despesas = self.despesa_repositorio.listar_despesas()
        total = 0

        # Percorre as despesas cadastradas
        for id_despesa, dados in despesas.items():
            data = dados["data"]
            valor = dados["valor"]

            # Separa ano, mês e dia da data
            ano, mes, dia = data.split("-")

            ano_data = int(ano)
            mes_data = int(mes)

            # Soma despesas do período selecionado
            if ano_data == self.ano and mes_data == self.mes:
                total += valor

        return total

    def calcular_saldo(self):
        # Calcula receitas menos despesas
        saldo = self.calcular_receitas() - self.calcular_despesas()
        return saldo

    def verificar_deficit(self):
        # Verifica se o saldo é negativo
        return self.calcular_saldo() < 0

    def comparar_receita_prevista(self):
        # Compara receita realizada e prevista
        receita_realizada = self.calcular_receitas()

        if receita_realizada == self.receita_prevista:
            return "Previsão de receita acertada!"

        elif receita_realizada > self.receita_prevista:
            return "A receita realizada superou a previsão!"

        else:
            return "A receita realizada ficou abaixo da previsão."

    def verificar_meta_economia(self):
        # Obtém a meta de economia configurada
        configuracoes = carregar_configuracoes()
        percentual = configuracoes["meta_economia_mensal"]

        receita_realizada = self.calcular_receitas()
        saldo = self.calcular_saldo()

        # Calcula o valor mínimo da meta
        valor_meta = receita_realizada * (percentual / 100)

        # Verifica se a meta foi atingida
        if saldo >= valor_meta:
            return True

        return False
