import json
from pathlib import Path


class Alerta_Repositorio:
    def __init__(self, caminho=None):
        # Define o caminho do arquivo de armazenamento
        if caminho is None:
            self.caminho = Path("data/alertas.json")
        else:
            self.caminho = Path(caminho)

        # Carrega os alertas existentes
        self.alertas = self.carregar()

    def carregar(self):
        # Recupera os alertas do arquivo JSON, se existir
        if self.caminho.exists():
            with self.caminho.open("r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        else:
            return {}

    def salvar(self):
        # Garante que o diretório de armazenamento exista
        self.caminho.parent.mkdir(parents=True, exist_ok=True)

        # Persiste os alertas no arquivo JSON
        with self.caminho.open("w", encoding="utf-8") as arquivo:
            json.dump(
                self.alertas,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    def adicionar_alerta(self, alerta):
        # Gera um novo ID sequencial para o alerta
        if not self.alertas:
            novo_id = 1
        else:
            ids = [int(chave) for chave in self.alertas]
            novo_id = max(ids) + 1

        # Converte o alerta em dados serializáveis
        dados = {
            "tipo": alerta.tipo.value,
            "mensagem": alerta.mensagem,
            "data": alerta.data.isoformat()
        }

        # Registra e salva o novo alerta
        self.alertas[str(novo_id)] = dados
        self.salvar()

    def listar_alertas(self):
        # Retorna todos os alertas armazenados
        return self.alertas