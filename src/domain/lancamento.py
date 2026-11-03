
from src.domain.categoria import Categoria
from datetime import date


class Lancamento:
    """
    Classe base dos lançamentos financeiros.
    """

    def __init__(
        self,
        valor,
        categoria,
        data,
        descricao,
        forma_de_pagamento,
        id=None
    ):
        # Inicializa os atributos do lançamento
        self.valor = valor
        self.categoria = categoria
        self.data = data
        self.descricao = descricao
        self.forma_de_pagamento = forma_de_pagamento
        self.id = id

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, valor_cadastrado):
        # Impede valores não positivos
        if valor_cadastrado > 0:
            self.__valor = valor_cadastrado
        else:
            raise ValueError("O valor deve ser maior que 0")

    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, categoria_cadastrada):
        # Exige uma categoria válida
        if isinstance(categoria_cadastrada, Categoria):
            self.__categoria = categoria_cadastrada
        else:
            raise ValueError("O lançamento deve possuir uma categoria")

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data_cadastrada):
        # Valida o tipo da data
        if not isinstance(data_cadastrada, date):
            raise ValueError("Data não aceita")
        else:
            self.__data = data_cadastrada

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao_cadastrada):
        self.__descricao = descricao_cadastrada

    def __str__(self):
        # Formata os dados para exibição
        return (
            f"Valor: R$ {self.valor:.2f} | "
            f"Categoria: {self.categoria.nome} | "
            f"Data: {self.data} | "
            f"Descrição: {self.descricao} | "
            f"Forma de pagamento: {self.forma_de_pagamento}"
        )

    def to_dict(self):
        # Converte o lançamento em dicionário
        return {
            "valor": self.valor,
            "categoria_id": self.categoria.id,
            "data": self.data.isoformat(),
            "descricao": self.descricao,
            "forma_de_pagamento": self.forma_de_pagamento,
            "id": self.id,
        }

    @classmethod
    def from_dict(cls, dados, categoria_repositorio):
        # Recupera a categoria associada
        categoria = categoria_repositorio.buscar_por_id(
            dados["categoria_id"]
        )

        # Reconstrói o lançamento
        return cls(
            valor=dados["valor"],
            categoria=categoria,
            data=date.fromisoformat(dados["data"]),
            descricao=dados["descricao"],
            forma_de_pagamento=dados["forma_de_pagamento"],
            id=dados["id"],
        )
