from pathlib import Path
import json
from src.repositories.categoria_repository import Categoria_Repositorio
from src.domain.receita import Receita


class Receita_Repositorio:
    def __init__(self, categoria_repositorio):
        # Define o armazenamento e o repositório de categorias
        self.caminho = Path("data/receitas.json")
        self.categoria_repositorio = categoria_repositorio
        self.receitas = self.carregar()

    def carregar(self):
        # Recupera as receitas do JSON, se existir
        if self.caminho.exists():
            with self.caminho.open("r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        else:
            return {}

    def _converter_para_receita(self, id_receita, dados):
        # Reconstrói a receita com seu ID e categoria correspondente
        dados_receita = dados.copy()

        dados_receita["id"] = int(id_receita)

        return Receita.from_dict(
            dados_receita,
            self.categoria_repositorio
        )

    def salvar(self):
        # Persiste as receitas no arquivo JSON
        with self.caminho.open("w", encoding="utf-8") as arquivo:
            json.dump(
                self.receitas,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    def adicionar_receita(self, receita):
        # Gera o próximo ID disponível
        if not self.receitas:
            novo_id = 1
        else:
            lista = []
            for chave, dados in self.receitas.items():
                chave = int(chave)
                lista.append(chave)

            maior_id = max(lista)
            novo_id = maior_id + 1

        # Atribui o ID e prepara os dados para armazenamento
        receita.id = novo_id
        dados = receita.to_dict()
        dados.pop("id")

        # Registra a receita e salva as alterações
        self.receitas[str(novo_id)] = dados
        self.salvar()

    def listar_receitas(self):
        # Retorna todas as receitas armazenadas
        return self.receitas

    def excluir_receita(self, id):
        # Verifica se a receita existe antes da exclusão
        id_receita = str(id)

        if id_receita not in self.receitas:
            raise ValueError("Receita não encontrada")

        # Remove a receita e persiste a alteração
        self.receitas.pop(id_receita)
        self.salvar()