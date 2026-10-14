from enum import Enum


class TipoCategoria(Enum):
    RECEITA = "RECEITA"
    DESPESA = "DESPESA"


class Categoria:
    """
    Representa uma classificação utilizada para organizar
    as receitas e despesas do sistema.

    Possui um nome, um tipo (RECEITA ou DESPESA), uma descrição
    opcional e um limite financeiro mensal quando se trata
    de uma categoria de despesa.

    Permite organizar os lançamentos e acompanhar os gastos
    associados a cada categoria, possibilitando a verificação
    de limites e a geração de alertas.
    """

    def __init__(self, nome, tipo, descricao, limite):
        self.nome = nome
        self.tipo = tipo
        self.descricao = descricao
        self.limite = limite

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome_cadastrado):
        if nome_cadastrado.strip() != "":
            self.__nome = nome_cadastrado
        else:
            raise ValueError("O nome da categoria não pode ser vazio")

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo_cadastrado):
        if isinstance(tipo_cadastrado, TipoCategoria):
            self.__tipo = tipo_cadastrado
        else:
            raise ValueError("O tipo deve ser RECEITA ou DESPESA")

    @property
    def limite(self):
        return self.__limite

    @limite.setter
    def limite(self, limite_cadastrado):
        if self.tipo == TipoCategoria.RECEITA:
            self.__limite = None

        elif limite_cadastrado is not None and limite_cadastrado > 0:
            self.__limite = limite_cadastrado

        else:
            raise ValueError("O limite da despesa deve ser maior que 0")

    def criar(self):
        pass

    def editar(self):
        pass

    def excluir(self):
        pass