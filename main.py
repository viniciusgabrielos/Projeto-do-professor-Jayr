from src.repositories.categoria_repository import Categoria_Repositorio
import argparse
from datetime import datetime
from src.domain.despesa import Despesa
from src.repositories.despesa_repository import Despesa_Repositorio
from src.domain.categoria import Categoria


def main():
    parser = argparse.ArgumentParser(
        prog="financas",
        description="Sistema de controle financeiro"
    )

    subparsers = parser.add_subparsers(
        dest="comando",
        required=True
    )

    subparsers.add_parser("adicionar-despesa")
    subparsers.add_parser("listar-categorias")
    subparsers.add_parser("relatorio-mensal")

    argumentos = parser.parse_args()

    if argumentos.comando == "adicionar-despesa":
        print("---Cadastro de Despesa---")
        while True:
            
            try:

                valor = float(input("Valor da despesa: R$ "))

                if valor > 0:
                    break

                print("O valor deve ser maior que 0. Tente novamente.")

            except ValueError:
                print("Valor inválido! Digite um número válido.")
       
        repositorio_categorias = Categoria_Repositorio()
        categorias = repositorio_categorias.listar()

        print("\nCategorias disponíveis para despesas:")

        for id_cat, dados in categorias.items():
            if dados["tipo"] == "DESPESA":
                print(
                f"ID: {id_cat} | "
                f"Nome: {dados['nome']} | "
                f"Limite: R$ {dados['limite']:.2f}" )

        id_categoria = input("\nID da categoria: ")

        if id_categoria not in categorias:
            raise ValueError("Categoria não encontrada")

        dados_categoria = categorias[id_categoria]

        if dados_categoria["tipo"] != "DESPESA":
            raise ValueError("A categoria selecionada não é do tipo DESPESA")

        categoria = Categoria.from_dict({
        **dados_categoria,
        "id": int(id_categoria)
})
        while True:
            try:
                data_despesa = datetime.strptime(
            input("Data da despesa (DD-MM-AAAA): "),
            "%d-%m-%Y"
                ).date()

                break

            except ValueError:
                print("Data inválida! Digite no formato DD-MM-AAAA.")

        
        descricao = input("Descrição da despesa: ").strip()

           
        while True:
            forma_de_pagamento = input("Forma de pagamento: ").strip()

            if forma_de_pagamento:
                break

            print("A forma de pagamento não pode ser vazia. Tente novamente.")

        despesa = Despesa(valor=valor,categoria=categoria,data=data_despesa,descricao=descricao,forma_de_pagamento=forma_de_pagamento)
        repositorio_despesas = Despesa_Repositorio()
        repositorio_despesas.adicionar_despesa(despesa)

        print("Despesa cadastrada com sucesso!")
        print("Id da despesa:", despesa.id)
  
    elif argumentos.comando == "listar-categorias":
        repositorio = Categoria_Repositorio()
        categorias = repositorio.listar()

        if not categorias:
            print("Nenhuma categoria cadastrada.")
        else:
            for id_categoria, dados in categorias.items():
                print(
                f"ID: {id_categoria} | "
                f"Nome: {dados['nome']} | "
                f"Tipo: {dados['tipo']} | "
                f"Limite: {dados['limite']}"
            )
    else:
        print(f"Comando '{argumentos.comando}' ainda não implementado.")


if __name__ == "__main__":
    main()
