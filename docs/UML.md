
# UML — Sistema de Controle Financeiro

```mermaid
classDiagram
    direction TB

    class Lancamento {
        -valor
        -categoria
        -data
        -descricao
        -forma_de_pagamento
        -id
        +__str()__
        +to_dict()
        +from_dict()
    }

    class Receita
    class Despesa

    class Categoria {
        -nome
        -tipo
        -descricao
        -limite
        -id
        +to_dict()
        +from_dict()
        +__str__()
        +__eq__()
        +__contains__()
        +__len__()
    }

    class TipoCategoria {
        <<enumeration>>
        RECEITA
        DESPESA
    }

    class OrcamentoMensal {
        -mes
        -ano
        -receita_prevista
        +calcular_receitas()
        +calcular_despesas()
        +calcular_saldo()
        +verificar_deficit()
        +comparar_receita_prevista()
        +verificar_meta_economia()
    }

    class SaldoAtual {
        +calcular_saldo()
    }

    class Relatorio {
        +calcular_despesas_por_categoria()
        +calcular_percentual_por_categoria()
        +identificar_mes_mais_economico()
        +comparar_ultimos_meses()
    }

    class Alerta {
        -tipo
        -mensagem
        -data
    }

    class TipoAlerta {
        <<enumeration>>
        ALTO_VALOR
        LIMITE_EXCEDIDO
        DEFICIT_ORCAMENTARIO
        PREVISAO_RECEITA
        META_ECONOMIA
    }

    Lancamento <|-- Receita
    Lancamento <|-- Despesa

    Lancamento "0..*" --> "1" Categoria : possui
    Categoria --> TipoCategoria : possui tipo
    Alerta --> TipoAlerta : possui tipo

    OrcamentoMensal ..> Receita : consulta dados
    OrcamentoMensal ..> Despesa : consulta dados

    SaldoAtual ..> Receita : consulta dados
    SaldoAtual ..> Despesa : consulta dados

    Relatorio ..> Receita : consulta dados
    Relatorio ..> Despesa : consulta dados
    Relatorio ..> Categoria : consulta dados

    Alerta ..> Despesa : pode ser gerado por
    Alerta ..> Categoria : verifica limite
    Alerta ..> OrcamentoMensal : utiliza informações
```

## Relações entre as classes

As setas do diagrama representam os relacionamentos e as dependências entre as classes do domínio:

- **Herança:** `Receita` e `Despesa` herdam os atributos e comportamentos de `Lancamento`.
- **Associação:** cada `Lancamento` possui uma `Categoria`, que determina sua classificação como receita ou despesa.
- **Dependência:** `OrcamentoMensal`, `SaldoAtual` e `Relatorio` utilizam informações de receitas, despesas e categorias para realizar seus cálculos e consultas.

### Relação com os repositórios

Embora os repositórios não estejam representados diretamente no diagrama, eles são responsáveis pela persistência e recuperação dos dados utilizados pelas classes:

- `Receita_Repositorio`: armazenamento, listagem e exclusão de receitas.
- `Despesa_Repositorio`: armazenamento, listagem e exclusão de despesas.
- `Categoria_Repositorio`: armazenamento, consulta, edição e exclusão de categorias.
- `Orcamento_Repositorio`: armazenamento e recuperação de orçamentos mensais.
- `Alerta_Repositorio`: armazenamento e recuperação dos alertas gerados pelo sistema.

As setas tracejadas representam dependências e consultas realizadas por meio desses repositórios, e não necessariamente associações diretas entre objetos. Dessa forma, o diagrama mantém o foco nas classes do domínio, enquanto os repositórios são descritos separadamente.
