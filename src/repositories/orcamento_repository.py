
from pathlib import Path
import json


class Orcamento_Repositorio:

    def __init__(self):
        self.caminho = Path("data/orcamentos.json")
        self.orcamentos = self.carregar()

    def carregar(self):
        if self.caminho.exists():
            with self.caminho.open("r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        else:
            return {}

    def salvar(self):
        with self.caminho.open("w", encoding="utf-8") as arquivo:
            json.dump(
                self.orcamentos,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    def adicionar_orcamento(self, mes, ano, receita_prevista):
        chave = f"{ano}-{mes:02d}"

        if chave in self.orcamentos:
            raise ValueError("Já existe um orçamento para esse mês")

        if not isinstance(receita_prevista, (int, float)) or isinstance(receita_prevista, bool):
            raise ValueError("A receita prevista deve ser numérica")

        if receita_prevista < 0:
            raise ValueError("A receita prevista não pode ser negativa")

        self.orcamentos[chave] = {
            "mes": mes,
            "ano": ano,
            "receita_prevista": receita_prevista
        }

        self.salvar()

    def buscar_orcamento(self, mes, ano):
        chave = f"{ano}-{mes:02d}"
        return self.orcamentos.get(chave)
