
class Lancamento:
    """
    Classe base que representa um lançamento financeiro do sistema.

    Armazena as informações comuns às movimentações financeiras,
    como valor, categoria, data, descrição e forma de pagamento.

    Serve como classe-pai para Receita e Despesa, permitindo
    reutilizar características e comportamentos comuns entre
    os dois tipos de lançamento.
    """
    pass


class Receita(Lancamento):
    """
    Representa uma entrada de dinheiro no controle financeiro.

    Herda as características básicas de Lancamento e permite
    registrar valores recebidos pelo usuário, como salário,
    trabalhos extras ou outras fontes de renda.

    Suas informações são utilizadas no cálculo do saldo
    financeiro e no acompanhamento do orçamento mensal.
    """
    pass


class Despesa(Lancamento):
    """
    Representa uma saída de dinheiro no controle financeiro.

    Herda as características básicas de Lancamento e permite
    registrar gastos realizados pelo usuário, como alimentação,
    transporte, moradia e lazer.

    Participa do cálculo dos gastos diários e mensais, podendo
    gerar alertas quando ultrapassa limites financeiros
    estabelecidos pelo sistema.
    """
    pass


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
    pass


class OrcamentoMensal:
    """
    Representa o planejamento financeiro de um determinado mês.

    Reúne as previsões de receitas e despesas e os lançamentos
    financeiros associados ao período.

    É responsável por fornecer os cálculos de receitas,
    despesas e saldo disponível, permitindo acompanhar
    a situação financeira mensal e identificar possíveis
    déficits no orçamento.
    """
    pass


class SaldoDiario:
    """
    Representa a consulta do saldo financeiro de um determinado dia.

    Utiliza as receitas e despesas registradas na data
    correspondente para calcular o resultado financeiro diário.

    Permite verificar a movimentação do dia sem precisar
    armazenar um saldo fixo, pois o valor pode ser obtido
    a partir dos lançamentos associados à data.
    """
    pass


class Relatorio:
    """
    Representa a estrutura responsável pela geração de
    relatórios e estatísticas financeiras do sistema.

    Utiliza os lançamentos e os orçamentos mensais para
    organizar informações sobre receitas, despesas e
    comportamento financeiro do usuário.

    Permite consultar gastos por categoria, analisar formas
    de pagamento, calcular percentuais de despesas,
    identificar o mês com menor gasto e comparar os
    resultados financeiros dos últimos meses.
    """
    pass


class Alerta:
    """
    Representa uma notificação gerada quando uma regra
    financeira definida pelo sistema é identificada.

    Armazena informações como data de emissão, mensagem
    e tipo de alerta.

    Pode representar situações como despesas de alto valor,
    ultrapassagem do limite de uma categoria ou saldo mensal
    negativo.

    Permite emitir a notificação ao usuário e registrar
    o alerta para consulta posterior.
    """
    pass