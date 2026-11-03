import json
from pathlib import Path

from src.domain.categoria import Categoria, TipoCategoria


class Categoria_Repositorio:
    def __init__(self):
        # Define o arquivo de armazenamento e carrega as categorias
        self.caminho = Path("data/categorias.json")
        self.categorias = self.carregar()

    def carregar(self):
        # Recupera as categorias do JSON, se existir
        if self.caminho.exists():
            with self.caminho.open("r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        else:
            return {}

    def salvar(self):
        # Persiste as categorias no arquivo JSON
        with self.caminho.open("w", encoding="utf-8") as arquivo:
            json.dump(
                self.categorias,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    def _existe_categoria_equivalente(self, categoria, id_categoria_a_ignorar=None):
        # Verifica categorias equivalentes, ignorando um ID quando necessário
        for chave, dados in self.categorias.items():
            if (
                id_categoria_a_ignorar is not None
                and chave == str(id_categoria_a_ignorar)
            ):
                continue

            # Reconstrói a categoria armazenada para comparação
            dados_categoria = dados.copy()
            dados_categoria["id"] = int(chave)

            categoria_existente = Categoria.from_dict(dados_categoria)

            if categoria == categoria_existente:
                return True
        return False

    def adicionar(self, categoria):
        # Impede o cadastro de categorias duplicadas
        if self._existe_categoria_equivalente(categoria):
            raise ValueError("Já existe uma categoria com esse nome e tipo")

        # Gera o próximo ID disponível
        if not self.categorias:
            novo_id = 1
        else:
            lista = []

            for chave in self.categorias.keys():
                chave = int(chave)
                lista.append(chave)

            maior_id = max(lista)
            novo_id = maior_id + 1

        # Atribui o ID e prepara os dados para armazenamento
        categoria.id = novo_id

        dados = categoria.to_dict()
        dados.pop("id")

        # Registra a categoria e salva as alterações
        self.categorias[str(novo_id)] = dados

        self.salvar()

    def listar(self):
        # Retorna todas as categorias armazenadas
        return self.categorias

    def buscar_por_id(self, id_categoria):
        # Normaliza o ID e verifica sua existência
        id_categoria = str(id_categoria)

        if id_categoria not in self.categorias:
            raise ValueError("Categoria não encontrada")

        # Reconstrói e retorna o objeto Categoria
        dados = self.categorias[id_categoria].copy()
        dados["id"] = int(id_categoria)

        return Categoria.from_dict(dados)

    def editar(self, id_categoria, alteracoes):
        # Verifica se a categoria existe
        id_categoria = str(id_categoria)

        if id_categoria not in self.categorias:
            raise ValueError("Categoria não encontrada")

        # Define os campos que podem ser alterados
        campos_permitidos = {
            "nome",
            "descricao",
            "limite"
        }

        # Impede alterações em campos não permitidos
        for campo in alteracoes:
            if campo not in campos_permitidos:
                raise ValueError(f"Campo inválido: {campo}")

        # Aplica as alterações aos dados atuais
        dados_atuais = self.categorias[id_categoria].copy()
        dados_atuais.update(alteracoes)

        dados_atuais["id"] = int(id_categoria)

        # Reconstrói o objeto para validar os novos dados
        categoria_atualizada = Categoria.from_dict(dados_atuais)

        # Evita duplicidade com outras categorias
        if self._existe_categoria_equivalente(
            categoria_atualizada,
            id_categoria_a_ignorar=id_categoria
        ):
            raise ValueError(
                "Já existe uma categoria com esse nome e tipo"
            )

        # Atualiza os dados e persiste no arquivo
        dados = categoria_atualizada.to_dict()
        dados.pop("id")

        self.categorias[id_categoria] = dados
        self.salvar()

        return categoria_atualizada

    def excluir(self, id_categoria):
        # Verifica a existência antes de excluir
        id_categoria = str(id_categoria)
        if id_categoria not in self.categorias:
            raise ValueError("Categoria não encontrada")

        # Remove a categoria e salva as alterações
        self.categorias.pop(id_categoria)
        self.salvar()