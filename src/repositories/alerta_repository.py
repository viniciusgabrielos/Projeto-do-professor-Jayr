import json
from pathlib import Path


class Alerta_Repositorio:
    def __init__(self, caminho=None):
        if caminho is None:
            self.caminho = Path("data/alertas.json")
        else:
            self.caminho = Path(caminho)

        self.alertas = self.carregar()

    def carregar(self):
        if self.caminho.exists():
            with self.caminho.open("r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        else:
            return {}

    def salvar(self):
        self.caminho.parent.mkdir(parents=True, exist_ok=True)

        with self.caminho.open("w", encoding="utf-8") as arquivo:
            json.dump(
                self.alertas,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    def adicionar_alerta(self, alerta):
        if not self.alertas:
            novo_id = 1
        else:
            ids = [int(chave) for chave in self.alertas]
            novo_id = max(ids) + 1

        dados = {
            "tipo": alerta.tipo.value,
            "mensagem": alerta.mensagem,
            "data": alerta.data.isoformat()
        }

        self.alertas[str(novo_id)] = dados
        self.salvar()

    def listar_alertas(self):
        return self.alertas