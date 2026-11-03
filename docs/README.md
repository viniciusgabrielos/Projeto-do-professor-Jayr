# Sistema de Controle Financeiro Pessoal

## Sobre o projeto

Sistema de controle financeiro pessoal desenvolvido em Python como projeto acadêmico da disciplina de Programação Orientada a Objetos (POO).

O sistema permite registrar receitas e despesas, organizar categorias financeiras, acompanhar o saldo acumulado, cadastrar orçamentos mensais e gerar relatórios e alertas relacionados à movimentação financeira. É necessária a leitura completa desse material para um melhor aproveitamento do sistema.

## Objetivo

Aplicar conceitos de Programação Orientada a Objetos, como encapsulamento, herança, abstração e organização de responsabilidades, por meio do desenvolvimento de uma aplicação de controle financeiro pessoal.

## Funcionalidades

- Cadastro, listagem e exclusão de receitas e despesas.
- Gerenciamento de categorias financeiras.
- Classificação de categorias entre receitas e despesas.
- Definição de limites mensais para categorias de despesas.
- Cadastro de previsão de receitas por mês.
- Consulta ao saldo financeiro acumulado.
- Fechamento e análise financeira do mês atual.
- Relatórios de despesas por categoria e percentuais.
- Identificação do mês mais econômico.
- Comparação de receitas e despesas dos últimos meses.
- Geração de alertas financeiros.

## Tecnologias utilizadas

- Python
- JSON para persistência de dados
- Argparse para interface de comandos no terminal
- Pytest para testes automatizados

## Arquitetura e modelagem

O projeto utiliza uma organização baseada em classes de domínio e repositórios, separando as regras e cálculos financeiros da persistência dos dados.

### Classes principais

- **Lancamento:** classe-base de receitas e despesas. Possui validações de valor, categoria e data, além de métodos de conversão de dados.
- **Receita:** representa entradas financeiras e herda os atributos e comportamentos de `Lancamento`. Exige uma categoria do tipo receita.
- **Despesa:** representa saídas financeiras e herda os atributos e comportamentos de `Lancamento`. Exige uma categoria do tipo despesa.
- **Categoria:** representa a classificação dos lançamentos, contendo nome, tipo, descrição e limite. Categorias de despesas possuem limite positivo, enquanto categorias de receitas não possuem limite.
- **OrcamentoMensal:** realiza cálculos financeiros de determinado mês, incluindo receitas, despesas, saldo, déficit, comparação com receita prevista e meta de economia.
- **SaldoAtual:** calcula o saldo financeiro acumulado considerando todas as receitas e despesas registradas.
- **Relatorio:** organiza informações financeiras, como despesas por categoria, percentuais, mês mais econômico e comparativos mensais.
- **Alerta:** representa avisos financeiros gerados pelo sistema, utilizando tipos definidos pelo enum `TipoAlerta`.

### Diagrama UML

O diagrama UML completo, com as classes de domínio e seus relacionamentos, está disponível em:

[Visualizar UML](UML.md)

As dependências relacionadas aos repositórios são explicadas no próprio documento.

## Estrutura do projeto

```text
Projeto-do-professor-Jayr/
│
├── data/
│   ├── alertas.json
│   ├── categorias.json
│   ├── despesas.json
│   ├── orcamentos.json
│   ├── receitas.json
│   └── settings.json
│
├── docs/
│   ├── README.md
│   └── UML.md
│
├── src/
│   ├── domain/
│   │   ├── alerta.py
│   │   ├── categoria.py
│   │   ├── despesa.py
│   │   ├── lancamento.py
│   │   ├── orcamento_mensal.py
│   │   ├── receita.py
│   │   ├── regras_alertas.py
│   │   ├── relatorio.py
│   │   ├── saldo_atual.py
│   │   └── settings.py
│   │
│   └── repositories/
│       ├── alerta_repository.py
│       ├── categoria_repository.py
│       ├── despesa_repository.py
│       ├── orcamento_repository.py
│       └── receita_repository.py
│
├── test/
│   ├── test_alerta.py
│   ├── test_categoria.py
│   ├── test_heranca.py
│   ├── test_lancamento.py
│   ├── test_orcamento_mensal.py
│   └── test_relatorio.py
│
├── main.py
└── .gitignore
```

## Instalação e execução

### Pré-requisitos

- Python 3 instalado.
- Git instalado, caso o projeto seja baixado diretamente pelo repositório.

### 1. Clonar o repositório

```bash
git clone https://github.com/viniciusgabrielos/Projeto-do-professor-Jayr
```

### 2. Acessar a pasta do projeto

```bash
cd Projeto_do_professor_Jayr
```

### 3. Executar o sistema

```bash
python main.py
```

O comando apresenta a ajuda do sistema quando nenhum subcomando é informado.

## Comandos disponíveis

Todos os comandos devem ser executados no terminal, a partir da pasta principal do projeto, utilizando a seguinte estrutura:

```bash
python main.py comando
```

Para consultar os comandos disponíveis:

```bash
python main.py --help
```

| Comando | Finalidade |
|---|---|
| `adicionar-receita` | Cadastra uma receita, solicitando os dados necessários. |
| `adicionar-despesa` | Cadastra uma despesa e verifica possíveis alertas financeiros. |
| `excluir-receita` | Exclui uma receita cadastrada. |
| `excluir-despesa` | Exclui uma despesa cadastrada. |
| `listar-lancamentos` | Lista as receitas e despesas registradas. |
| `listar-categorias` | Lista as categorias cadastradas. |
| `adicionar-categoria` | Cadastra uma nova categoria. |
| `editar-categoria` | Edita informações de uma categoria existente. |
| `excluir-categoria` | Exclui uma categoria não associada a lançamentos. |
| `adicionar-orcamento` | Cadastra uma previsão de receita para determinado mês e ano. |
| `fechar-mes` | Realiza a análise financeira do mês atual. |
| `consultar-saldo` | Consulta o saldo financeiro acumulado. |
| `relatorio-mensal` | Apresenta informações e comparações financeiras mensais. |

### Exemplos

```bash
python main.py adicionar-receita
```

```bash
python main.py adicionar-despesa
```

```bash
python main.py consultar-saldo
```

## Persistência e configurações

O sistema utiliza arquivos JSON para armazenar os dados financeiros.

| Arquivo | Conteúdo |
|---|---|
| `receitas.json` | Receitas cadastradas. |
| `despesas.json` | Despesas cadastradas. |
| `categorias.json` | Categorias financeiras. |
| `orcamentos.json` | Orçamentos mensais. |
| `alertas.json` | Alertas gerados. |
| `settings.json` | Configurações do sistema. |

As configurações incluem:

- `limite_alerta_alto_valor`: valor mínimo para geração de alerta de alto gasto.
- `meses_comparacao`: quantidade de meses considerados nos comparativos.
- `meta_economia_mensal`: percentual da receita realizada utilizado como meta de economia.

## Alertas financeiros

Os alertas são representados pela classe `Alerta`, enquanto as regras de geração estão separadas no módulo `regras_alertas.py`.

| Tipo de alerta | Critério |
|---|---|
| Alto valor | Uma despesa individual atinge ou ultrapassa o limite configurado. |
| Limite excedido | O total de despesas de uma categoria ultrapassa seu limite mensal. |
| Déficit orçamentário | As despesas mensais superam as receitas. |
| Previsão de receita | Informa se a receita realizada atingiu a previsão cadastrada. |
| Meta de economia | Informa se o saldo atingiu a meta de economia estabelecida. |

### Quando os alertas são gerados?

- **Cadastro de despesa:** verifica alertas de alto valor e limite excedido.
- **Fechamento mensal:** verifica déficit, compara a receita realizada com a previsão e avalia a meta de economia.

Os alertas gerados são armazenados em `alertas.json`.

## Testes

O projeto utiliza Pytest para testes automatizados das classes e funcionalidades do domínio.

Para executar os testes, utilize:

```bash
pytest -q
```

### Cobertura dos testes

Os testes automatizados estão organizados em arquivos que verificam as principais funcionalidades do sistema:

- **`test_alerta.py`**: testa a criação, validação e persistência de alertas, além das regras de geração de alertas de alto valor e limite excedido por categoria.
- **`test_categoria_repository.py`**: verifica o cadastro, prevenção de duplicidade, edição e identificação de categorias, incluindo os métodos especiais `__len__` e `__contains__`.
- **`test_lancamento.py`**: testa a criação e validação de lançamentos, receitas e despesas, incluindo a herança e a compatibilidade entre categorias e tipos de lançamento.
- **`test_orcamento_mensal.py`**: verifica os cálculos de receitas, despesas, saldo e déficit mensal, além da separação dos lançamentos por período.
- **`test_relatorio.py`**: testa os cálculos de despesas e percentuais por categoria, identificação do mês mais econômico e comparação entre períodos, incluindo a virada do ano.

## Decisões de design

- **Orçamento mensal:** o orçamento é cadastrado previamente para um mês e ano. O fechamento mensal é realizado manualmente e considera somente o mês atual. Para realizar o fechamento, é necessário que exista um orçamento previamente cadastrado para o período. Assim, é responsabilidade do usuário adicionar orçamento e depois, preferencialmente, no último dia do mês, realizar o comando de fechar o mês. Sem esse passo a passo, há um comprometimento de algumas funcionalidades, como a falta da emissão do alerta do saldo mensal ser negativo.
- **Receitas e despesas:** o sistema permite cadastrar, listar e excluir receitas e despesas, mas não possui funcionalidade de edição desses lançamentos.
- **Dados iniciais (seeds):** os arquivos JSON disponibilizados no projeto contêm dados iniciais que permitem executar e testar as funcionalidades do sistema sem precisar cadastrar todas as informações manualmente desde o início.
- **Main.py:** todos os comandos no main.py podem ser acessados usando "python main.py comando-escolhido", com exceção do adicionar-orcamento, é necessário informar além do comando, mês que está fazendo o orçamento, o ano e a receita prevista para esse mês, assim:
```bash
python main.py adicionar-orcamento 10 2026 4000
```
Nesse exemplo, o usuário está adicionando um orçamento do mês de outubro, do ano de 2026 e está prevendo que irá receber 4000 reais. 
É interessante que isso seja feito no início de cada mês.

## Autor

Vinicius Gabriel Oliveira Santos