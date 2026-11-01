
from src.repositories.categoria_repository import Categoria_Repositorio
import argparse
from datetime import datetime, date
from src.domain.despesa import Despesa
from src.repositories.despesa_repository import Despesa_Repositorio
from src.domain.categoria import Categoria,TipoCategoria
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
from src.domain.saldo_atual import SaldoAtual
from src.domain import relatorio



def main():
    parser = argparse.ArgumentParser(
        prog="financas",
        description="Sistema de controle financeiro"
    )

    subparsers = parser.add_subparsers(
        dest="comando",
        required=True
    )

    # 1. Receitas e despesas
    subparsers.add_parser("adicionar-despesa")
    subparsers.add_parser("adicionar-receita")
    subparsers.add_parser("excluir-despesa")
    subparsers.add_parser("excluir-receita")
    subparsers.add_parser("listar-lancamentos")

    # 2. Categorias
    subparsers.add_parser("listar-categorias")
    subparsers.add_parser("adicionar-categoria")
    subparsers.add_parser("editar-categoria")
    subparsers.add_parser("excluir-categoria")

    # 3. Orçamentos
    parser_orcamento = subparsers.add_parser("adicionar-orcamento")
    parser_orcamento.add_argument("mes", type=int)
    parser_orcamento.add_argument("ano", type=int)
    parser_orcamento.add_argument("receita_prevista", type=float)

    subparsers.add_parser("mostrar-orcamentos")
    subparsers.add_parser("fechar-mes")

    # 4. Saldo
    subparsers.add_parser("consultar-saldo")

    # 5. Relatórios
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
    
            if (id_categoria in categorias and categorias[id_categoria]["tipo"] == "RECEITA"
                ):
                break
    
            print("ID inválido ou categoria não encontrada."
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
    
            print("A forma de pagamento não pode ser vazia. "
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
    

    elif argumentos.comando == "excluir-despesa":
        categoria_repositorio = Categoria_Repositorio()
        despesa_repositorio = Despesa_Repositorio(categoria_repositorio)

        despesas = despesa_repositorio.listar_despesas()

        if not despesas:
            print("Não existem despesas cadastradas.")
        else:
            print("\n--- Despesas cadastradas ---")

            for id_despesa, dados in despesas.items():
                despesa = despesa_repositorio._converter_para_despesa(id_despesa, dados)
                print(f"ID: {id_despesa} | {despesa}")

            id_despesa = input("\nDigite o ID da despesa que deseja excluir: "
        )

            try:
                despesa_repositorio.excluir_despesa(id_despesa)
                print("Despesa excluída com sucesso!")
            except ValueError as erro:
                print(erro)

    elif argumentos.comando == "excluir-receita":
        categoria_repositorio = Categoria_Repositorio()
        receita_repositorio = Receita_Repositorio(categoria_repositorio)

        receitas = receita_repositorio.listar_receitas()

        if not receitas:
            print("Não existem receitas cadastradas.")
        else:
            print("\n--- Receitas cadastradas ---")

            for id_receita, dados in receitas.items():

                receita = receita_repositorio._converter_para_receita(
                id_receita, dados
            )
                print(f"ID: {id_receita} | {receita}")

            id_receita = input("\nDigite o ID da receita que deseja excluir: ")

            try:
                receita_repositorio.excluir_receita(id_receita)
                print("Receita excluída com sucesso!")
            except ValueError as erro:
                print(erro)

    elif argumentos.comando == "listar-lancamentos":
        categoria_repositorio = Categoria_Repositorio()
        receita_repositorio = Receita_Repositorio(categoria_repositorio)
        despesa_repositorio = Despesa_Repositorio(categoria_repositorio)

        receitas = receita_repositorio.listar_receitas()
        despesas = despesa_repositorio.listar_despesas()

        if not receitas and not despesas:
            print("Não existem lançamentos cadastrados.")
        else:
            print("\n========== LANÇAMENTOS ==========")

            print("\n--- RECEITAS ---")

            if receitas:
                for id_receita, dados in receitas.items():

                    receita = receita_repositorio._converter_para_receita(
                    id_receita, dados
                )
                    print(f"ID: {id_receita} | {receita}")
            else:
                print("Nenhuma receita cadastrada.")

            print("\n--- DESPESAS ---")

            if despesas:
                for id_despesa, dados in despesas.items():

                    despesa = despesa_repositorio._converter_para_despesa(
                    id_despesa, dados
                )
                    print(f"ID: {id_despesa} | {despesa}")
            else:
                print("Nenhuma despesa cadastrada.")
    
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

    elif argumentos.comando == "adicionar-categoria":
        print("--- Cadastro de Categoria ---")

        while True:
            nome = input("Nome da categoria: ").strip()

            if nome:
                break

            print("O nome da categoria não pode ser vazio.")

        while True:
            tipo_escolhido = input(
            "Tipo da categoria (RECEITA/DESPESA): "
        ).strip().upper()

            if tipo_escolhido == "RECEITA":
                tipo = TipoCategoria.RECEITA
                break

            elif tipo_escolhido == "DESPESA":
                tipo = TipoCategoria.DESPESA
                break

            print("Tipo inválido. Digite RECEITA ou DESPESA.")

        descricao = input("Descrição da categoria (opcional): "
    ).strip()

        if tipo == TipoCategoria.DESPESA:
            while True:
                try:
                    limite = float(input("Limite mensal da categoria: R$ ")
                )

                    if limite > 0:
                        break

                    print("O limite deve ser maior que zero.")

                except ValueError:
                    print("Digite um valor numérico válido.")
        else:
            limite = None

        try:
            categoria = Categoria(
            nome=nome,
            tipo=tipo,
            descricao=descricao,
            limite=limite
        )

            categoria_repositorio = Categoria_Repositorio()
            categoria_repositorio.adicionar(categoria)

            print("Categoria cadastrada com sucesso!")
            print(f"ID da categoria: {categoria.id}")

        except ValueError as erro:
            print(erro)

    elif argumentos.comando == "editar-categoria":
        categoria_repositorio = Categoria_Repositorio()
        categorias = categoria_repositorio.listar()

        if not categorias:
            print("Não existem categorias cadastradas.")
            return

        print("\n========== CATEGORIAS ==========")

        for id_categoria in categorias:
            categoria = categoria_repositorio.buscar_por_id(id_categoria)
            print(categoria)

        id_escolhido = input(
            "\nDigite o ID da categoria que deseja editar: "
    )

        try:
            categoria = categoria_repositorio.buscar_por_id(id_escolhido)

        except ValueError as erro:
            print(erro)
            return

        print("\nCampos disponíveis: nome, descricao, limite")

        campo = input(
            "Qual campo deseja editar? "
        ).strip().lower()

        campos_permitidos = {
        "nome",
        "descricao",
        "limite"
    }

        if campo not in campos_permitidos:
            print("Campo inválido.")
            return

        if campo == "nome":
            novo_valor = input("Novo nome: ").strip()

            if not novo_valor:
                print("O nome não pode ser vazio.")
                return

        elif campo == "descricao":
            novo_valor = input("Nova descrição: ").strip()
            novo_valor = novo_valor if novo_valor else None

        elif campo == "limite":
            if categoria.tipo == TipoCategoria.RECEITA:
                print("Categorias de receita não possuem limite.")
                return

            while True:
                try:
                    novo_valor = float(
                        input("Novo limite mensal: R$ ")
                )

                    if novo_valor > 0:
                        break

                    print("O limite deve ser maior que zero.")

                except ValueError:
                    print("Digite um valor numérico válido.")

        alteracoes = {campo: novo_valor}

        try:
            categoria_atualizada = categoria_repositorio.editar(
            id_escolhido,
            alteracoes
        )

            print("\nCategoria atualizada com sucesso!")
            print(categoria_atualizada)

        except ValueError as erro:
            print(erro)


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

    
    elif argumentos.comando == "consultar-saldo":
        repositorio_categorias = Categoria_Repositorio()

        repositorio_receitas = Receita_Repositorio(
        repositorio_categorias
    )

        repositorio_despesas = Despesa_Repositorio(
        repositorio_categorias
    )

        saldo = SaldoAtual(
        repositorio_receitas,
        repositorio_despesas
    )

        resultado = saldo.calcular_saldo()

        print("\n--- Saldo Financeiro ---")
        print(f"Saldo atual: R$ {resultado:.2f}")


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
            return
       
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

    elif argumentos.comando == "relatorio-mensal":
        print("\n--- Relatório Financeiro ---")

        repositorio_categorias = Categoria_Repositorio()
        repositorio_receitas = Receita_Repositorio(repositorio_categorias)
        repositorio_despesas = Despesa_Repositorio(repositorio_categorias)

        relatorio_financeiro = relatorio.Relatorio(
        repositorio_receitas,
        repositorio_despesas
    )

    
        despesas_categoria = (
        relatorio_financeiro.calcular_despesas_por_categoria()
    )
        percentuais = (
        relatorio_financeiro.calcular_percentual_por_categoria()
    )

        print("\n--- Despesas por Categoria ---")

        if not despesas_categoria:
            print("Nenhuma despesa cadastrada.")
        else:
            for categoria, valor in despesas_categoria.items():
                percentual = percentuais[categoria]
                print(
                f"{categoria}: R$ {valor:.2f} "
                f"({percentual:.2f}%)"
            )

    
        mes_economico = (
        relatorio_financeiro.identificar_mes_mais_economico()
    )

        print("\n--- Mês Mais Econômico ---")

        if mes_economico is None:
            print("Não existem despesas para realizar a comparação.")
        else:
            print(
            f"{mes_economico['mes']:02d}/{mes_economico['ano']}: "
            f"R$ {mes_economico['total_despesas']:.2f}"
        )

   
        comparacao = (
        relatorio_financeiro.comparar_ultimos_meses()
    )

        print("\n--- Receitas e Despesas dos Últimos Meses ---")

        for mes, valores in comparacao.items():
            print(f"\nMês: {mes}")
            print(f"Receitas: R$ {valores['receitas']:.2f}")
            print(f"Despesas: R$ {valores['despesas']:.2f}")
    
    else:
        print(
            f"Comando '{argumentos.comando}' "
            "ainda não implementado."
            )
if __name__ == "__main__":
    main()
