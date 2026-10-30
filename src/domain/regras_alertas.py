
from src.domain.alerta import Alerta, TipoAlerta
from src.domain.settings import carregar_configuracoes
from datetime import date


def verificar_alerta_alto_valor(despesa, repositorio_alertas):
    configuracoes = carregar_configuracoes()
    limite = configuracoes["limite_alerta_alto_valor"]

    if despesa.valor >= limite:
        alerta = Alerta(
            tipo=TipoAlerta.ALTO_VALOR,
            mensagem=(
                f"Despesa de alto valor: R$ {despesa.valor:.2f}"
            )
        )

        repositorio_alertas.adicionar_alerta(alerta)
        return alerta

    return None
def verificar_alerta_limite_excedido(
    despesa,
    repositorio_despesas,
    repositorio_alertas
):
    categorias = repositorio_despesas.categoria_repositorio.listar()

    categoria = categorias[str(despesa.categoria.id)]
    limite = categoria["limite"]

    total_categoria = 0

    despesas = repositorio_despesas.listar_despesas()

    for id_despesa, dados in despesas.items():
        if dados["categoria_id"] == despesa.categoria.id:
            data_despesa = date.fromisoformat(dados["data"])

            if (
                data_despesa.month == despesa.data.month
                and data_despesa.year == despesa.data.year
            ):
                total_categoria += dados["valor"]

    if total_categoria > limite:
        alerta = Alerta(
            tipo=TipoAlerta.LIMITE_EXCEDIDO,
            mensagem=(
                f"Limite da categoria {categoria['nome']} excedido. "
                f"Total: R$ {total_categoria:.2f}"
            )
        )

        repositorio_alertas.adicionar_alerta(alerta)
        return alerta

    return None