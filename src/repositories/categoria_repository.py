
import json
from pathlib import Path

from src.domain.categoria import Categoria, TipoCategoria


class Categoria_Repositorio:
    def __init__(self):
        self.caminho = Path("data/categorias.json")
        self.categorias = self.carregar()

    def carregar(self):
        if self.caminho.exists():
            with self.caminho.open("r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        else:
            return {}

    def salvar(self):
        with self.caminho.open("w", encoding="utf-8") as arquivo:
            json.dump(
                self.categorias,
                arquivo,
                ensure_ascii=False,
                indent=4
            )
    def _existe_categoria_equivalente(self, categoria, id_categoria_a_ignorar=None
    ):
        for chave, dados in self.categorias.items():
            if (id_categoria_a_ignorar is not None and chave == str(id_categoria_a_ignorar)):
                continue
    
            dados_categoria = dados.copy()
            dados_categoria["id"] = int(chave)
    
            categoria_existente = Categoria.from_dict(dados_categoria)
    
            if categoria == categoria_existente:
                return True
        return False
    

    def adicionar(self, categoria):
        if self._existe_categoria_equivalente(categoria):
            raise ValueError("Já existe uma categoria com esse nome e tipo"
        )

        if not self.categorias:
            novo_id = 1
        else:
            lista = []

            for chave in self.categorias.keys():
                chave = int(chave)
                lista.append(chave)

            maior_id = max(lista)
            novo_id = maior_id + 1

        categoria.id = novo_id

        dados = categoria.to_dict()
        dados.pop("id")

        self.categorias[str(novo_id)] = dados

        self.salvar()
    
    def listar(self):
        return self.categorias

    def editar(self, id_categoria, alteracoes):
        id_categoria = str(id_categoria)

        if id_categoria not in self.categorias:
            raise ValueError("Categoria não encontrada")

        campos_permitidos = {
            "nome",
            "tipo",
            "descricao",
            "limite"
        }

        for campo in alteracoes:
            if campo not in campos_permitidos:
                raise ValueError(f"Campo inválido: {campo}")

        dados_atuais = self.categorias[id_categoria].copy()
        dados_atuais.update(alteracoes)

        dados_atuais["id"] = int(id_categoria)

        if isinstance(dados_atuais["tipo"], str):
            dados_atuais["tipo"] = TipoCategoria(
                dados_atuais["tipo"].upper()
            )

        categoria_atualizada = Categoria.from_dict(dados_atuais)

        
        if self._existe_categoria_equivalente(categoria_atualizada,id_categoria_a_ignorar=id_categoria):raise ValueError(
        "Já existe uma categoria com esse nome e tipo"
    )

        dados = categoria_atualizada.to_dict()
        dados.pop("id")

        self.categorias[id_categoria] = dados
        self.salvar()

        return categoria_atualizada

    def excluir(self, id_categoria):
        id_categoria = str(id_categoria)
        if id_categoria not in self.categorias:
            raise ValueError("Categoria não encontrada")

        self.categorias.pop(id_categoria)
        self.salvar()