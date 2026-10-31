
from datetime import date


class Relatorio:
    """
    Representa a estrutura responsável pela geração de
    relatórios e estatísticas financeiras do sistema.

    Permite consultar despesas por categoria, calcular
    percentuais de despesas, identificar o mês mais econômico
    e comparar receitas e despesas dos últimos três meses.
    """

    def __init__(self, receita_repositorio, despesa_repositorio):
        self.receita_repositorio = receita_repositorio
        self.despesa_repositorio = despesa_repositorio

    def calcular_despesas_por_categoria(self):
        categorias = self.despesa_repositorio.categoria_repositorio.listar()
        despesas = self.despesa_repositorio.listar_despesas()

        totais = {}

        for id_despesa, dados in despesas.items():
            categoria_id = dados["categoria_id"]
            valor = dados["valor"]

            categoria = categorias[str(categoria_id)]

            if categoria["tipo"] == "DESPESA":
                nome_categoria = categoria["nome"]

                totais[nome_categoria] = (
                    totais.get(nome_categoria, 0) + valor
                )

        return totais

    def calcular_percentual_por_categoria(self):
        totais = self.calcular_despesas_por_categoria()

        total_despesas = sum(totais.values())

        if total_despesas == 0:
            return {}

        percentuais = {}

        for categoria, valor in totais.items():
            percentuais[categoria] = round(
                (valor / total_despesas) * 100, 2
            )

        return percentuais

    def identificar_mes_mais_economico(self):
        despesas = self.despesa_repositorio.listar_despesas()

        totais_por_mes = {}

        for dados in despesas.values():
            data_despesa = date.fromisoformat(dados["data"])
            chave_mes = (data_despesa.year, data_despesa.month)

            totais_por_mes[chave_mes] = (
                totais_por_mes.get(chave_mes, 0) + dados["valor"]
            )

        if not totais_por_mes:
            return None

        mes_mais_economico = min(
            totais_por_mes,
            key=totais_por_mes.get
        )

        ano, mes = mes_mais_economico

        return {
            "mes": mes,
            "ano": ano,
            "total_despesas": totais_por_mes[mes_mais_economico]
        }

    def _obter_ultimos_tres_meses(self):
        hoje = date.today()
        meses = []

        for deslocamento in range(2, -1, -1):
            indice_mes = hoje.year * 12 + (hoje.month - 1) - deslocamento
            ano, mes = divmod(indice_mes, 12)

            meses.append((ano, mes + 1))

        return meses

    def comparar_ultimos_tres_meses(self):
        meses = self._obter_ultimos_tres_meses()

        resultado = {
            (ano, mes): {
                "receitas": 0,
                "despesas": 0
            }
            for ano, mes in meses
        }

        receitas = self.receita_repositorio.listar_receitas()
        despesas = self.despesa_repositorio.listar_despesas()

        for dados in receitas.values():
            data_receita = date.fromisoformat(dados["data"])
            chave_mes = (data_receita.year, data_receita.month)

            if chave_mes in resultado:
                resultado[chave_mes]["receitas"] += dados["valor"]

        for dados in despesas.values():
            data_despesa = date.fromisoformat(dados["data"])
            chave_mes = (data_despesa.year, data_despesa.month)

            if chave_mes in resultado:
                resultado[chave_mes]["despesas"] += dados["valor"]

        return {
            f"{mes:02d}/{ano}": valores
            for (ano, mes), valores in resultado.items()
        }
