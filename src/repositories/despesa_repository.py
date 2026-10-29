from pathlib import Path
import json


class Despesa_Repositorio:
    def __init__(self,categoria_repositorio):
        self.caminho = Path("data/despesas.json")
        self.categoria_repositorio = categoria_repositorio
        self.despesas = self.carregar()

    def carregar(self):
        if self.caminho.exists():
            with self.caminho.open("r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        else:
            return {}

    def salvar(self):
        with self.caminho.open("w", encoding="utf-8") as arquivo:
            json.dump(
                self.despesas,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    def adicionar_despesa(self, despesa):
        if not self.despesas:
            novo_id = 1
        else:
            lista = []
            for chave, dados in self.despesas.items():
                chave = int(chave)
                lista.append(chave)

            maior_id = max(lista)
            novo_id = maior_id + 1

        despesa.id = novo_id
        dados = despesa.to_dict()
        dados.pop("id")

        self.despesas[str(novo_id)] = dados
        self.salvar()

    def listar_despesas(self):
        return self.despesas

    def excluir_despesa(self, id):
        id_despesa = str(id)

        if id_despesa not in self.despesas:
            raise ValueError("Despesa não encontrada")

        self.despesas.pop(id_despesa)
        self.salvar()