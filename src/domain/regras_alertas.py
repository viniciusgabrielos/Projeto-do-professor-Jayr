
from datetime import date

from src.domain.alerta import Alerta, TipoAlerta
from src.domain.settings import carregar_configuracoes


def verificar_alerta_alto_valor(despesa, repositorio_alertas):
    # Obtém o limite configurado
    configuracoes = carregar_configuracoes()
    limite = configuracoes["limite_alerta_alto_valor"]

    # Verifica se a despesa atingiu o limite
    if despesa.valor >= limite:
        alerta = Alerta(
            tipo=TipoAlerta.ALTO_VALOR,
            mensagem=f"Despesa de alto valor: R$ {despesa.valor:.2f}"
        )

        repositorio_alertas.adicionar_alerta(alerta)
        return alerta

    return None


def verificar_alerta_limite_excedido(
    despesa,
    repositorio_despesas,
    repositorio_alertas
):
    # Recupera os dados da categoria
    categorias = repositorio_despesas.categoria_repositorio.listar()

    categoria = categorias[str(despesa.categoria.id)]
    limite = categoria["limite"]

    total_categoria = 0

    despesas = repositorio_despesas.listar_despesas()

    # Soma despesas da categoria no mesmo mês
    for id_despesa, dados in despesas.items():
        if dados["categoria_id"] == despesa.categoria.id:
            data_despesa = date.fromisoformat(dados["data"])

            if (
                data_despesa.month == despesa.data.month
                and data_despesa.year == despesa.data.year
            ):
                total_categoria += dados["valor"]

    # Verifica se o limite mensal foi ultrapassado
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


def verificar_alerta_deficit_orcamentario(
    data_referencia,
    repositorio_receitas,
    repositorio_despesas,
    repositorio_alertas
):
    total_receitas = 0
    total_despesas = 0

    # Soma receitas do mês de referência
    for dados in repositorio_receitas.listar_receitas().values():
        data_receita = date.fromisoformat(dados["data"])

        if (
            data_receita.month == data_referencia.month
            and data_receita.year == data_referencia.year
        ):
            total_receitas += dados["valor"]

    # Soma despesas do mês de referência
    for dados in repositorio_despesas.listar_despesas().values():
        data_despesa = date.fromisoformat(dados["data"])

        if (
            data_despesa.month == data_referencia.month
            and data_despesa.year == data_referencia.year
        ):
            total_despesas += dados["valor"]

    # Calcula o saldo mensal
    saldo = total_receitas - total_despesas

    # Gera alerta se houver déficit
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


def verificar_alerta_previsao_receita(orcamento, repositorio_alertas):
    # Compara receita realizada e prevista
    resultado = orcamento.comparar_receita_prevista()

    alerta = Alerta(
        tipo=TipoAlerta.PREVISAO_RECEITA,
        mensagem=resultado
    )

    repositorio_alertas.adicionar_alerta(alerta)

    return alerta


def verificar_alerta_meta_economia(orcamento, repositorio_alertas):
    # Verifica se a meta foi atingida
    meta_atingida = orcamento.verificar_meta_economia()

    # Define a mensagem conforme o resultado
    if meta_atingida:
        mensagem = "Meta de economia mensal atingida!"
    else:
        mensagem = "Meta de economia mensal não atingida."

    alerta = Alerta(
        tipo=TipoAlerta.META_ECONOMIA,
        mensagem=mensagem
    )

    repositorio_alertas.adicionar_alerta(alerta)

    return alerta
