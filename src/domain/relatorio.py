
from datetime import date
from src.domain.settings import carregar_configuracoes


class Relatorio:
    """
    Responsável pela geração de relatórios financeiros.
    """

    def __init__(self, receita_repositorio, despesa_repositorio):
        # Inicializa os repositórios utilizados
        self.receita_repositorio = receita_repositorio
        self.despesa_repositorio = despesa_repositorio

    def calcular_despesas_por_categoria(self):
        # Recupera categorias e despesas
        categorias = self.despesa_repositorio.categoria_repositorio.listar()
        despesas = self.despesa_repositorio.listar_despesas()

        totais = {}

        # Agrupa despesas por categoria
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
        # Obtém os totais por categoria
        totais = self.calcular_despesas_por_categoria()

        total_despesas = sum(totais.values())

        # Evita divisão por zero
        if total_despesas == 0:
            return {}

        percentuais = {}

        # Calcula a participação de cada categoria
        for categoria, valor in totais.items():
            percentuais[categoria] = round(
                (valor / total_despesas) * 100, 2
            )

        return percentuais

    def identificar_mes_mais_economico(self):
        despesas = self.despesa_repositorio.listar_despesas()

        totais_por_mes = {}

        # Agrupa despesas por mês e ano
        for dados in despesas.values():
            data_despesa = date.fromisoformat(dados["data"])
            chave_mes = (data_despesa.year, data_despesa.month)

            totais_por_mes[chave_mes] = (
                totais_por_mes.get(chave_mes, 0) + dados["valor"]
            )

        # Retorna None se não houver despesas
        if not totais_por_mes:
            return None

        # Identifica o mês com menor despesa
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

    def _obter_ultimos_meses(self):
        # Obtém a quantidade de meses configurada
        configuracoes = carregar_configuracoes()
        quantidade_meses = configuracoes["meses_comparacao"]

        hoje = date.today()
        meses = []

        # Monta os meses em ordem cronológica
        for deslocamento in range(quantidade_meses - 1, -1, -1):
            indice_mes = hoje.year * 12 + (hoje.month - 1) - deslocamento
            ano, mes = divmod(indice_mes, 12)

            meses.append((ano, mes + 1))

        return meses

    def comparar_ultimos_meses(self):
        # Obtém os meses para comparação
        meses = self._obter_ultimos_meses()

        # Inicializa receitas e despesas de cada mês
        resultado = {
            (ano, mes): {
                "receitas": 0,
                "despesas": 0
            }
            for ano, mes in meses
        }

        receitas = self.receita_repositorio.listar_receitas()
        despesas = self.despesa_repositorio.listar_despesas()

        # Distribui receitas pelos meses correspondentes
        for dados in receitas.values():
            data_receita = date.fromisoformat(dados["data"])
            chave_mes = (data_receita.year, data_receita.month)

            if chave_mes in resultado:
                resultado[chave_mes]["receitas"] += dados["valor"]

        # Distribui despesas pelos meses correspondentes
        for dados in despesas.values():
            data_despesa = date.fromisoformat(dados["data"])
            chave_mes = (data_despesa.year, data_despesa.month)

            if chave_mes in resultado:
                resultado[chave_mes]["despesas"] += dados["valor"]

        # Formata os meses para exibição
        return {
            f"{mes:02d}/{ano}": valores
            for (ano, mes), valores in resultado.items()
        }
