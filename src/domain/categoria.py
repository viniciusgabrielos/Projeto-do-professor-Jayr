
from enum import Enum


class TipoCategoria(Enum):
    RECEITA = "RECEITA"
    DESPESA = "DESPESA"


class Categoria:
    """
    Representa uma classificação utilizada para organizar
    as receitas e despesas do sistema.

    Possui nome, tipo, descrição opcional e limite mensal
    para categorias de despesas.
    """

    def __init__(self, nome, tipo, descricao=None, limite=None, id=None):
        # Inicializa os atributos da categoria
        self.nome = nome
        self.tipo = tipo
        self.descricao = descricao if descricao else None
        self.limite = limite
        self.id = id

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome_cadastrado):
        # Valida e normaliza o nome
        if not isinstance(nome_cadastrado, str) or not nome_cadastrado.strip():
            raise ValueError("O nome da categoria não pode ser vazio")

        self.__nome = nome_cadastrado.strip()

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo_cadastrado):
        # Aceita apenas tipos definidos no enum
        if isinstance(tipo_cadastrado, TipoCategoria):
            self.__tipo = tipo_cadastrado
        else:
            raise ValueError("O tipo deve ser RECEITA ou DESPESA")

    @property
    def limite(self):
        return self.__limite

    @limite.setter
    def limite(self, limite_cadastrado):
        # Categorias de receita não possuem limite
        if self.tipo == TipoCategoria.RECEITA:
            self.__limite = None

        # Valida o limite das categorias de despesa
        elif (
            isinstance(limite_cadastrado, (int, float))
            and not isinstance(limite_cadastrado, bool)
            and limite_cadastrado > 0
        ):
            self.__limite = limite_cadastrado

        else:
            raise ValueError("O limite da despesa deve ser maior que 0")

    def to_dict(self):
        # Converte a categoria em dicionário
        return {
            "nome": self.nome,
            "tipo": self.tipo.value,
            "descricao": self.descricao,
            "limite": self.limite,
            "id": self.id,
        }

    @classmethod
    def from_dict(cls, dados):
        # Reconstrói a categoria a partir dos dados
        return cls(
            nome=dados["nome"],
            tipo=TipoCategoria(dados["tipo"]),
            descricao=dados["descricao"],
            limite=dados["limite"],
            id=dados["id"],
        )

    def __eq__(self, outra):
        # Compara categorias pelo nome e tipo
        if not isinstance(outra, Categoria):
            return NotImplemented

        mesmo_nome = (
            self.nome.strip().casefold()
            == outra.nome.strip().casefold()
        )

        mesmo_tipo = self.tipo == outra.tipo

        return mesmo_nome and mesmo_tipo

    def __str__(self):
        # Formata a categoria para exibição
        return (
            f"ID: {self.id} | "
            f"Nome: {self.nome} | "
            f"Tipo: {self.tipo.value} | "
            f"Limite: R$ {self.limite:.2f}"
            if self.limite is not None
            else
            f"ID: {self.id} | "
            f"Nome: {self.nome} | "
            f"Tipo: {self.tipo.value} | "
            "Limite: Não possui"
        )

    def __len__(self):
        # Retorna o tamanho do nome
        return len(self.nome)

    def __contains__(self, item):
        # Verifica se o texto está no nome
        return item.casefold() in self.nome.casefold()
