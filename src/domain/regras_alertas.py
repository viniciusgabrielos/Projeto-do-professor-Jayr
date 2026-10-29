
from src.domain.alerta import Alerta, TipoAlerta
from src.domain.settings import carregar_configuracoes


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
