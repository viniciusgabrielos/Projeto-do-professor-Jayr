
from pathlib import Path
import json
from src.repositories.categoria_repository import Categoria_Repositorio
from src.domain.receita import Receita

class Receita_Repositorio:
    def __init__(self,categoria_repositorio):
        self.caminho = Path("data/receitas.json")
        self.categoria_repositorio = categoria_repositorio
        self.receitas = self.carregar()

    def carregar(self):
        if self.caminho.exists():
            with self.caminho.open("r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        else:
            return {}

    def _converter_para_receita(self, id_receita, dados):
        dados_receita = dados.copy()

        dados_receita["id"] = int(id_receita)

        return Receita.from_dict(
        dados_receita,
        self.categoria_repositorio
    )

    def salvar(self):
        with self.caminho.open("w", encoding="utf-8") as arquivo:
            json.dump(
                self.receitas,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    def adicionar_receita(self, receita):
        if not self.receitas:
            novo_id = 1
        else:
            lista = []
            for chave, dados in self.receitas.items():
                chave = int(chave)
                lista.append(chave)

            maior_id = max(lista)
            novo_id = maior_id + 1

        receita.id = novo_id
        dados = receita.to_dict()
        dados.pop("id")

        self.receitas[str(novo_id)] = dados
        self.salvar()

    def listar_receitas(self):
        return self.receitas

    def excluir_receita(self, id):
        id_receita = str(id)

        if id_receita not in self.receitas:
            raise ValueError("Receita não encontrada")

        self.receitas.pop(id_receita)
        self.salvar()
