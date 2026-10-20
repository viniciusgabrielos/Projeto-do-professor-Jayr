
from datetime import date

from src.domain.categoria import Categoria, TipoCategoria
from src.domain.receita import Receita
from src.domain.despesa import Despesa


categoria_despesa = Categoria(
    nome="Alimentação",
    tipo=TipoCategoria.DESPESA,
    descricao="Gastos com alimentação",
    limite=800
)

categoria_receita = Categoria(
    nome="Aulas",
    tipo=TipoCategoria.RECEITA,
    descricao="Recebimentos por aulas"
)


receita = Receita(
    valor=2000,
    categoria=categoria_receita,
    data=date.today(),
    descricao="Aulas particulares",
    forma_de_pagamento="PIX"
)

despesa = Despesa(
    valor=300,
    categoria=categoria_despesa,
    data=date.today(),
    descricao="Compras do mês",
    forma_de_pagamento="Débito"
)


print(receita)
print(despesa)

assert receita.valor == 2000
assert despesa.valor == 300

assert receita.categoria is categoria_receita
assert despesa.categoria is categoria_despesa

print("Testes de criação e herança concluídos!")


print("\n--- Testando validações herdadas ---")

try:
    Despesa(
        valor=-100,
        categoria=categoria_despesa,
        data=date.today(),
        descricao="Teste inválido",
        forma_de_pagamento="PIX"
    )
except ValueError as erro:
    print("Valor inválido rejeitado:", erro)
else:
    raise AssertionError("A despesa deveria rejeitar valor negativo")

