import json
from pathlib import Path

class Categoria_Repositorio:   

    def __init__(self):
        self.caminho = Path("data/categorias.json")
        self.categorias = self.carregar()

    def carregar(self):
        if self.caminho.exists():
            with self.caminho.open("r",encoding = "utf-8") as arquivo:
                return json.load(arquivo)
        else:
            return {}

    def salvar(self):
        with self.caminho.open("w",encoding = "utf-8") as arquivo:
            json.dump(self.categorias,arquivo, ensure_ascii= False, indent=4)