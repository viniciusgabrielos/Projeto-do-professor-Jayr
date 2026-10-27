
from pathlib import Path
import json


class Receita_Repositorio:
    def __init__(self):
        self.caminho = Path("data/receitas.json")
        self.receitas = self.carregar()

    def carregar(self):
        if self.caminho.exists():
            with self.caminho.open("r", encoding="utf-8") as arquivo:
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
