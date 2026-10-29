from src.domain.categoria import Categoria
from datetime import date

class Lancamento:
    """
    Classe base que representa um lançamento financeiro do sistema.

    Armazena as informações comuns às movimentações financeiras,
    como valor, categoria, data, descrição e forma de pagamento.

    Serve como classe-pai para Receita e Despesa, permitindo
    reutilizar características e comportamentos comuns entre
    os dois tipos de lançamento.
    """
   

    def __init__(self, valor, categoria, data, descricao, forma_de_pagamento,id = None):
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
        if valor_cadastrado > 0:
            self.__valor = valor_cadastrado
        else:
            raise ValueError("O valor deve ser maior que 0")

   

    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, categoria_cadastrada):
        if isinstance(categoria_cadastrada,Categoria):
            self.__categoria = categoria_cadastrada
        else:
            raise ValueError("O lançamento deve possuir uma categoria")

  

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data_cadastrada):
        if not isinstance(data_cadastrada,date):
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
        return(
            f"Valor: R$ {self.valor:.2f} | "
            f"Categoria: {self.categoria.nome} | "
            f"Data: {self.data} | "
            f"Descrição: {self.descricao} | "
            f"Forma de pagamento: {self.forma_de_pagamento}"
        )

    def to_dict(self):
            return {
                "valor": self.valor,
                "categoria_id": self.categoria.id,
                "data": self.data.isoformat(),
                "descricao": self.descricao,
                "forma_de_pagamento": self.forma_de_pagamento,
                "id": self.id,
            }
    @classmethod
    def from_dict(cls, dados):
        categoria = Categoria.from_dict(dados["categoria"])

        return cls(
            valor=dados["valor"],
            categoria=categoria,
            data=date.fromisoformat(dados["data"]),
            descricao=dados["descricao"],
            forma_de_pagamento=dados["forma_de_pagamento"],
            id=dados["id"],
    )