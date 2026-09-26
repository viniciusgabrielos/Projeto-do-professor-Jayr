````md
```mermaid
classDiagram

    class Lancamento {
        - valor
        - categoria
        - data
        - descricao
        - formaPagamento
        + cadastrar()
        + editar()
        + excluir()
    }

    class Receita {
        + cadastrarReceita()
        + editarReceita()
    }

    class Despesa {
        + cadastrarDespesa()
        + editarDespesa()
    }

    class Categoria {
        - nome
        - tipo
        - descricao
        - limite
        + criar()
        + editar()
        + excluir()
    }

    class OrcamentoMensal {
        - mes
        - previsaoReceitas
        - previsaoDespesas
        + calcularTotalReceita()
        + calcularTotalDespesa()
        + calcularSaldo()
    }

    class SaldoDiario {
        - dia
        + consultarSaldo()
    }

    class Relatorio {
        - mes
        + mostrarDespesaPorCategoria()
        + mostrarDespesaPorFormaPagamento()
        + mostrarPercentualCategoria()
        + mostrarMesMaisEconomico()
        + mostrarComparativoUltimos3Meses()
    }

    class Alerta {
        - data
        - mensagem
        - tipo
    }


    Lancamento <|-- Receita
    Lancamento <|-- Despesa

    Categoria "1" <-- "0..*" Lancamento
    OrcamentoMensal "1" <-- "0..*" Lancamento
    SaldoDiario "1" <-- "0..*" Lancamento
    Relatorio "1" <-- "0..*" Lancamento
    Relatorio "1" <-- "0..*" OrcamentoMensal

    Despesa "1" <-- "0..*" Alerta
    Categoria "1" <-- "0..*" Alerta
    OrcamentoMensal "1" <-- "0..*" Alerta```



## Relações entre as classes

* **Receita e Despesa → Lançamento:** `Receita` e `Despesa` são tipos de `Lançamento`. Por isso, as duas herdam as características básicas de um lançamento financeiro.

* **Lançamento → Categoria:** cada lançamento está ligado a uma categoria, como alimentação, transporte, salário ou lazer. Uma categoria pode ter vários lançamentos.

* **Lançamento → OrçamentoMensal:** os lançamentos ficam associados ao orçamento do mês em que foram registrados. Um orçamento mensal pode reunir vários lançamentos.

* **Lançamento → SaldoDiario:** o saldo de um determinado dia é calculado a partir dos lançamentos daquele dia.

* **Relatorio → Lançamento:** os relatórios utilizam os lançamentos para organizar e apresentar informações, como despesas por categoria ou por forma de pagamento.

* **Relatorio → OrçamentoMensal:** os relatórios também utilizam os orçamentos mensais para fazer comparações entre meses e identificar informações como o mês com menor gasto.

* **Despesa → Alerta:** uma despesa pode gerar um alerta, por exemplo, quando ultrapassa o valor definido para um alerta de alto gasto.

* **Categoria → Alerta:** uma categoria pode gerar um alerta quando suas despesas ultrapassam o limite estabelecido.

* **OrçamentoMensal → Alerta:** um orçamento mensal pode gerar um alerta quando o saldo do mês fica negativo.

De forma geral, `Lancamento` é a parte central do sistema, pois as receitas e despesas são tipos de lançamento e várias outras classes utilizam essas informações para realizar seus cálculos e gerar consultas ou alertas.
