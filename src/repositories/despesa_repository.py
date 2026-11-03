from pathlib import Path
import json
from src.domain.despesa import Despesa


class Despesa_Repositorio:
    def __init__(self, categoria_repositorio):
        # Define o armazenamento e o repositório de categorias
        self.caminho = Path("data/despesas.json")
        self.categoria_repositorio = categoria_repositorio
        self.despesas = self.carregar()

    def carregar(self):
        # Recupera as despesas do JSON, se existir
        if self.caminho.exists():
            with self.caminho.open("r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        else:
            return {}

    def _converter_para_despesa(self, id_despesa, dados):
        # Reconstrói a despesa com seu ID e categoria correspondente
        dados_despesa = dados.copy()

        dados_despesa["id"] = int(id_despesa)

        return Despesa.from_dict(
            dados_despesa,
            self.categoria_repositorio
        )

    def salvar(self):
        # Persiste as despesas no arquivo JSON
        with self.caminho.open("w", encoding="utf-8") as arquivo:
            json.dump(
                self.despesas,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    def adicionar_despesa(self, despesa):
        # Gera o próximo ID disponível
        if not self.despesas:
            novo_id = 1
        else:
            lista = []
            for chave, dados in self.despesas.items():
                chave = int(chave)
                lista.append(chave)

            maior_id = max(lista)
            novo_id = maior_id + 1

        # Atribui o ID e prepara os dados para armazenamento
        despesa.id = novo_id
        dados = despesa.to_dict()
        dados.pop("id")

        # Registra a despesa e salva as alterações
        self.despesas[str(novo_id)] = dados
        self.salvar()

    def listar_despesas(self):
        # Retorna todas as despesas armazenadas
        return self.despesas

    def excluir_despesa(self, id):
        # Verifica se a despesa existe antes da exclusão
        id_despesa = str(id)

        if id_despesa not in self.despesas:
            raise ValueError("Despesa não encontrada")

        # Remove a despesa e persiste a alteração
        self.despesas.pop(id_despesa)
        self.salvar()