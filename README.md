# Sistema de Controle de Despesas Pessoais

## Diagrama UML
[Visualizar o UML](UML.md)

## Descrição

Projeto desenvolvido para a disciplina de Programação Orientada a Objetos (POO), com o objetivo de desenvolver um sistema para controle de despesas pessoais.

O sistema será utilizado para registrar receitas e despesas, organizar lançamentos por categorias, acompanhar o orçamento mensal, consultar saldos e gerar relatórios e alertas financeiros.

## Objetivo

O projeto tem como objetivo aplicar conceitos de Programação Orientada a Objetos na construção de um sistema de controle financeiro pessoal.

Entre os principais recursos planejados estão:

* Cadastro e gerenciamento de categorias;
* Registro de receitas e despesas como um lançamento;
* Controle do orçamento mensal;
* Consulta do saldo diário;
* Geração de relatórios financeiros;
* Geração de alertas para situações definidas pelo sistema.

## Modelagem

A estrutura do sistema foi planejada utilizando conceitos de Programação Orientada a Objetos, com definição de classes, atributos, métodos, herança e associações entre os elementos do sistema.

O diagrama UML apresenta visualmente a estrutura e os relacionamentos definidos para o projeto.

A descrição da responsabilidade de cada classe e sua estrutura inicial estão presentes no arquivo `classes.py`.

## Classes planejadas

* `Lancamento`

No lançamento, tem atributos de valor que recebe a quantidade que foi gasta ou ganha, associa-se com a classe catergoria, recebendo qual setor é essa receita ou essa despesa, há a data desse lançamento, uma pequena descrição e a forma que foi pago a despesa ou recebido a receita.

Os métodos resumem-se a criar, editar ou excluir determinado lançamento.

* `Receita`

Herda de lançamento.

Possui métodos próprios de criar e editar uma receita.
* `Despesa`

Herda de lançamento.

Possui métodos próprios de criar e editar uma despesa.

* `Categoria`

Possui nome, tipo, sendo uma receita ou uma despesa, descrição e um limite como atributos. Esse limite será associado ao tipo despesa.

Seus métodos consistem em criar, editar ou excluir essa categoria.
* `OrcamentoMensal`

Tem mês, uma previsão de receitas e uma previsão de despesas como atributos.

Tem métodos de calcular Receita total em um mês, calcular Despesa total em um mês e calcular um saldo de um mês, usando o balanço entre receitas e despesas de um mês.

* `SaldoDiario`

Tem como atributo o dia.

Seu método consiste em calcular o saldo daquele dia.

* `Relatorio`

Tem como atributo um mês.

Seus métodos consistem em mostrar despesa por categoria, mostrar despesa por forma de pagamento, mostrar gastos ou ganhos na forma percentual de acordo com cada categoria, mostrar mês mais econômico e mostrar um comparativo de gastos e ganhos nos últimos 3 meses.

* `Alerta`

Tem como atributo a data que ele foi emitido, a mensagem que aparecerá e o tipo, sendo esse tipo sendo um alerta pelo valor do lançamento de uma despesa ser alto, pelo valor limite ultrapassado em uma categoria, ou por um saldo mensal negativo.

Não há métodos.

## Estrutura do projeto

```text
Projeto-do-professor-Jayr/
│
├── README.md
├── .gitignore
├── UML.md
└── classes.py
```

