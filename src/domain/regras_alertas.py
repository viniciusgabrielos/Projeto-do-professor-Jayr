
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




from datetime import date
from src.domain.alerta import Alerta, TipoAlerta


def verificar_alerta_deficit_orcamentario(
    data_referencia,
    repositorio_receitas,
    repositorio_despesas,
    repositorio_alertas
):
    total_receitas = 0
    total_despesas = 0

    for dados in repositorio_receitas.listar_receitas().values():
        data_receita = date.fromisoformat(dados["data"])

        if (
            data_receita.month == data_referencia.month
            and data_receita.year == data_referencia.year
        ):
            total_receitas += dados["valor"]

    for dados in repositorio_despesas.listar_despesas().values():
        data_despesa = date.fromisoformat(dados["data"])

        if (
            data_despesa.month == data_referencia.month
            and data_despesa.year == data_referencia.year
        ):
            total_despesas += dados["valor"]

    saldo = total_receitas - total_despesas

    if saldo < 0:
        alerta = Alerta(
        tipo=TipoAlerta.DEFICIT_ORCAMENTARIO,
        mensagem=(
            f"Déficit orçamentário: despesas superaram "
            f"receitas em R$ {abs(saldo):.2f}"
        )
    )

        repositorio_alertas.adicionar_alerta(alerta)

    else:
        alerta = None

    return total_receitas, total_despesas, saldo, alerta