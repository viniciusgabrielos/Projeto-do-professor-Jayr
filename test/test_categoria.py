from src.domain.categoria import Categoria, TipoCategoria
from src.repositories.categoria_repository import Categoria_Repositorio


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

repositorio = Categoria_Repositorio()
dados_carregados = repositorio.carregar()

print("Dados carregados:", dados_carregados)

repositorio = Categoria_Repositorio()

try:
    repositorio.adicionar(categoria1)
except ValueError as erro:
    print("Duplicidade bloqueada:", erro)

print("ID atribuído:", categoria1.id)
print("Dados no repositório:", repositorio.categorias)

repositorio2 = Categoria_Repositorio()

print("Dados recuperados do JSON:", repositorio2.categorias)

print("\n--- Teste de mesmo nome, tipo diferente ---")

categoria_receita = Categoria(
    nome="Alimentação",
    tipo=TipoCategoria.RECEITA,
    descricao="Receita relacionada à alimentação"
)

repositorio.adicionar(categoria_receita)

print("Categoria cadastrada com ID:", categoria_receita.id)