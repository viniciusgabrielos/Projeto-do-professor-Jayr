
from src.repositories.categoria_repository import Categoria_Repositorio
import argparse
from datetime import datetime, date
from src.domain.despesa import Despesa
from src.repositories.despesa_repository import Despesa_Repositorio
from src.domain.categoria import Categoria
from src.domain.receita import Receita
from src.repositories.receita_repository import Receita_Repositorio
from src.repositories.alerta_repository import Alerta_Repositorio
from src.domain.regras_alertas import (
    verificar_alerta_alto_valor,
    verificar_alerta_limite_excedido,
    verificar_alerta_deficit_orcamentario,
    verificar_alerta_previsao_receita,
    verificar_alerta_meta_economia
)
from src.domain.orcamento_mensal import OrcamentoMensal
from src.repositories.orcamento_repository import Orcamento_Repositorio



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
    subparsers.add_parser("adicionar-receita")

    parser_orcamento = subparsers.add_parser("adicionar-orcamento")
    parser_orcamento.add_argument("mes", type=int)
    parser_orcamento.add_argument("ano", type=int)
    parser_orcamento.add_argument("receita_prevista", type=float)

    subparsers.add_parser("fechar-mes")
    subparsers.add_parser("relatorio-mensal")

    argumentos = parser.parse_args()

    if argumentos.comando == "adicionar-despesa":
        print("--- Cadastro de Despesa ---")

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

        tem_categoria_despesa = False

        for dados in categorias.values():
            if dados["tipo"] == "DESPESA":
                tem_categoria_despesa = True
                break

        if not tem_categoria_despesa:
            print("Nenhuma categoria de despesa cadastrada.")
            return

        print("\nCategorias disponíveis para despesas:")

        for id_cat, dados in categorias.items():
            if dados["tipo"] == "DESPESA":
                print(
                    f"ID: {id_cat} | "
                    f"Nome: {dados['nome']} | "
                    f"Limite: R$ {dados['limite']:.2f}"
                )

        while True:
            id_categoria = input("\nID da categoria: ")

            if (
                id_categoria in categorias
                and categorias[id_categoria]["tipo"] == "DESPESA"
            ):
                break

            print(
                "ID inválido ou categoria não encontrada. "
                "Tente novamente."
            )

        dados_categoria = categorias[id_categoria]

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

            print(
                "A forma de pagamento não pode ser vazia. "
                "Tente novamente."
            )

        despesa = Despesa(
            valor=valor,
            categoria=categoria,
            data=data_despesa,
            descricao=descricao,
            forma_de_pagamento=forma_de_pagamento
        )

        repositorio_despesas = Despesa_Repositorio(repositorio_categorias)
        repositorio_despesas.adicionar_despesa(despesa)
       
        repositorio_alertas = Alerta_Repositorio()

        alerta = verificar_alerta_alto_valor(despesa,repositorio_alertas)

        alerta_limite = verificar_alerta_limite_excedido(despesa,repositorio_despesas,repositorio_alertas
)

        print("Despesa cadastrada com sucesso!")
        print("ID da despesa:", despesa.id)

        if alerta is not None:
            print("ALERTA:", alerta.mensagem)

        if alerta_limite is not None:
            print("ALERTA:", alerta_limite.mensagem)

    elif argumentos.comando == "adicionar-receita":
        print("--- Cadastro de Receita ---")

        while True:
            try:
                valor = float(input("Valor da receita: R$ "))

                if valor > 0:
                    break

                print("O valor deve ser maior que 0. Tente novamente.")

            except ValueError:
                print("Valor inválido! Digite um número válido.")

        repositorio_categorias = Categoria_Repositorio()
        categorias = repositorio_categorias.listar()

        tem_categoria_receita = False

        for dados in categorias.values():
            if dados["tipo"] == "RECEITA":
                tem_categoria_receita = True
                break

        if not tem_categoria_receita:
            print("Nenhuma categoria de receita cadastrada.")
            return

        print("\nCategorias disponíveis para receitas:")

        for id_cat, dados in categorias.items():
            if dados["tipo"] == "RECEITA":
                print(
                    f"ID: {id_cat} | "
                    f"Nome: {dados['nome']}"
                )

        while True:
            id_categoria = input("\nID da categoria: ")

            if (
                id_categoria in categorias
                and categorias[id_categoria]["tipo"] == "RECEITA"
            ):
                break

            print(
                "ID inválido ou categoria não encontrada. "
                "Tente novamente."
            )

        dados_categoria = categorias[id_categoria]

        categoria = Categoria.from_dict({
            **dados_categoria,
            "id": int(id_categoria)
        })

        while True:
            try:
                data_receita = datetime.strptime(
                    input("Data da receita (DD-MM-AAAA): "),
                    "%d-%m-%Y"
                ).date()

                break

            except ValueError:
                print("Data inválida! Digite no formato DD-MM-AAAA.")

        descricao = input("Descrição da receita: ").strip()

        while True:
            forma_de_pagamento = input("Forma de pagamento: ").strip()

            if forma_de_pagamento:
                break

            print(
                "A forma de pagamento não pode ser vazia. "
                "Tente novamente."
            )

        receita = Receita(
            valor=valor,
            categoria=categoria,
            data=data_receita,
            descricao=descricao,
            forma_de_pagamento=forma_de_pagamento
        )

        repositorio_receitas = Receita_Repositorio(repositorio_categorias)
        repositorio_receitas.adicionar_receita(receita)

        print("Receita cadastrada com sucesso!")
        print("ID da receita:", receita.id)

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
    elif argumentos.comando == "adicionar-orcamento":
        try:
            repositorio_orcamentos = Orcamento_Repositorio()

            repositorio_orcamentos.adicionar_orcamento(
            argumentos.mes,
            argumentos.ano,
            argumentos.receita_prevista
        )

            print("Orçamento mensal cadastrado com sucesso!")

        except ValueError as erro:
            print(f"Erro: {erro}")
        
    elif argumentos.comando == "fechar-mes":
        print("--- Fechamento Mensal ---")

        repositorio_categorias = Categoria_Repositorio()
        repositorio_receitas = Receita_Repositorio(repositorio_categorias)
        repositorio_despesas = Despesa_Repositorio(repositorio_categorias)
        repositorio_alertas = Alerta_Repositorio()
        repositorio_orcamentos = Orcamento_Repositorio()

        data_referencia = date.today()

        dados_orcamento = repositorio_orcamentos.buscar_orcamento(
        data_referencia.month,
        data_referencia.year
    )

        if dados_orcamento is None:
            print("\n[ERRO] Não existe orçamento cadastrado para este mês.")

        else:
            receita_prevista = dados_orcamento["receita_prevista"]

        orcamento = OrcamentoMensal(
            mes=data_referencia.month,
            ano=data_referencia.year,
            receita_repositorio=repositorio_receitas,
            despesa_repositorio=repositorio_despesas,
            receita_prevista=receita_prevista
        )

        total_receitas = orcamento.calcular_receitas()
        total_despesas = orcamento.calcular_despesas()
        saldo = orcamento.calcular_saldo()

        alerta_deficit = verificar_alerta_deficit_orcamentario(
            data_referencia,
            repositorio_receitas,
            repositorio_despesas,
            repositorio_alertas
        )

        verificar_alerta_previsao_receita(
            orcamento,
            repositorio_alertas
        )

        verificar_alerta_meta_economia(
            orcamento,
            repositorio_alertas
        )

        print("\n--- Resultado do Fechamento Mensal ---")
        print(f"Receita prevista: R$ {receita_prevista:.2f}")
        print(f"Receitas realizadas: R$ {total_receitas:.2f}")
        print(f"Despesas: R$ {total_despesas:.2f}")
        print(f"Saldo: R$ {saldo:.2f}")

        if alerta_deficit[3] is not None:
            print("\nALERTA:", alerta_deficit[3].mensagem)
        else:
            print("\nNão houve déficit orçamentário.")

        print("\n" + orcamento.comparar_receita_prevista())

        if orcamento.verificar_meta_economia():
            print("Meta de economia mensal atingida!")
        else:
            print("Meta de economia mensal não atingida.")
    else:
        print(
            f"Comando '{argumentos.comando}' "
            "ainda não implementado."
            )
if __name__ == "__main__":
    main()
