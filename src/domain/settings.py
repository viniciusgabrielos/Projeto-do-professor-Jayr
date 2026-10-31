from pathlib import Path
import json


def carregar_configuracoes():
    caminho = Path(__file__).resolve().parents[2] / "data" / "settings.json"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        configuracoes = json.load(arquivo)

    limite = configuracoes["limite_alerta_alto_valor"]
    meses = configuracoes["meses_comparacao"]
    meta = configuracoes["meta_economia_mensal"]

    if type(limite) not in (int, float) or limite <= 0:
        raise ValueError("O limite de alto valor deve ser positivo")

    if type(meses) is not int or meses <= 0:
        raise ValueError("A quantidade de meses deve ser positiva")

    if type(meta) not in (int, float) or not 0 <= meta <= 100:
        raise ValueError("A meta de economia deve estar entre 0 e 100")

    return configuracoes