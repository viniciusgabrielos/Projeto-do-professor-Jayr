from pathlib import Path
import json

class Receita_Repositorio:
    def __init__(self):
        self.caminho = Path("data/receitas.json")
        self.receitas = self.carregar()

    def carregar(self):
        if self.caminho.exists():
            with self.caminho.open("r",encoding="utf-8") as arquivo:
                return json.load(arquivo)
        
        else:
            return {}

    def salvar(self):
            with self.caminho.open("w", encoding="utf-8") as arquivo:
                json.dump(
                    self.receitas,
                    arquivo,
                    ensure_ascii=False,
                    indent=4
                )
        