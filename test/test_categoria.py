from src.domain.categoria import Categoria, TipoCategoria


categoria1 = Categoria(
    nome="Alimentação",
    tipo=TipoCategoria.DESPESA,
    descricao="Gastos com mercado",
    limite=800
)


dados = categoria1.to_dict()
print("Dicionário:", dados)


nova_categoria = Categoria.from_dict(dados)


print("Nome:", nova_categoria.nome)
print("Tipo:", nova_categoria.tipo)
print("Descrição:", nova_categoria.descricao)
print("Limite:", nova_categoria.limite)
print("ID:", nova_categoria.id)

assert nova_categoria.nome == categoria1.nome
assert nova_categoria.tipo == categoria1.tipo
assert nova_categoria.descricao == categoria1.descricao
assert nova_categoria.limite == categoria1.limite

print("Teste de conversão concluído!")