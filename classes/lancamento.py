class Lancamento:
    """
    Classe base que representa um lançamento financeiro do sistema.

    Armazena as informações comuns às movimentações financeiras,
    como valor, categoria, data, descrição e forma de pagamento.

    Serve como classe-pai para Receita e Despesa, permitindo
    reutilizar características e comportamentos comuns entre
    os dois tipos de lançamento.
    """
    def _init_(self,valor, categoria, data, descricao, forma_de_pagamento):
        self._valor = valor
        self._categoria = categoria
        self.data = data
        self.descricao = descricao
        self.forma_de_pagamento = forma_de_pagamento

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self,valor_cadastrado):
        if valor_cadastrado > 0:
            self._valor = valor_cadastrado

        else:
            raise ValueError("O valor deve ser maior que 0")

    
    
