# AdaptaBrasil API — Coleta e Consumo de Dados

Projeto para automatizar a coleta e o consumo de dados da API do **AdaptaBrasil**, organizando os resultados em arquivos CSV por setor, indicador e tipo de desastre.

O processo completo é executado automaticamente através do `main.py`.

## Fluxo do projeto

O `main.py` executa todo o processo:

1. Lê a estrutura de indicadores do AdaptaBrasil.
2. Filtra os indicadores relevantes.
3. Consulta os endpoints da API.
4. Processa os dados retornados.
5. Salva os resultados organizados em `API/Data` e `API/output`.

Exemplos de categorias geradas:

```text
API/output/
├── Deslizamento de terra/
├── Inundações, enxurradas e alagamentos/
└── Risco de estresse hídrico/
```

## Estrutura

```text
Consumo-Api-AdaptaBrasil/
├── AdaptaBrasilAPIAccess/          # Acesso à estrutura da API do AdaptaBrasil
│   ├── AdaptaBrasilAPIAccess.py    # Script para obtenção da estrutura da API
│   ├── adaptaBrasilAPIEstrutura.csv # Estrutura dos indicadores
│   └── requirements.txt            # Dependências do módulo
├── API/
│   ├── Data/                       # Dados e indicadores processados
│   ├── output/                     # CSVs finais organizados por categoria
│   ├── coleta_dados.py             # Filtragem e preparação dos indicadores
│   └── consumo_api.py              # Consulta e processamento dos dados da API
├── main.py                         # Executa todo o processo de coleta
├── requirements.txt                # Dependências do projeto
├── readme.md                       # Documentação e instruções de uso
└── output.json                     # Dados de saída em formato JSON
```

## Pré-requisitos

* Python 3.9+
* `pip`
* `virtualenv`
* Git

## Instalação

### 1. Clone o repositório

clone o repositório necessário para obter a estrutura da API:

```bash
git clone https://github.com/AdaptaBrasil/AdaptaBrasilAPIAccess.git
```

Ao final, o diretório deve estar organizado desta forma:

```text
Consumo-Api-AdaptaBrasil/
├── AdaptaBrasilAPIAccess/
└── API/
```

### 2. Crie o ambiente virtual

Instale o `virtualenv`, caso ainda não esteja instalado:

```bash
pip install virtualenv
```

Crie o ambiente virtual na raiz do projeto:

```bash
virtualenv .venv
```

### 3. Ative o ambiente virtual

No Linux:

```bash
source .venv/bin/activate
```

Após a ativação, o terminal deverá indicar que o ambiente `.venv` está ativo.

### 4. Instale as dependências

Com o ambiente virtual ativado:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Execução

Com o ambiente virtual ativado, basta executar:

```bash
python main.py
```

O `main.py` executará automaticamente todo o processo de coleta e processamento dos dados.

Os arquivos gerados serão organizados principalmente em:

```text
API/Data/
API/output/
```

## Problemas comuns

### `virtualenv: command not found`

Instale o `virtualenv`:

```bash
pip install virtualenv
```

### `ModuleNotFoundError`

Verifique se o ambiente virtual está ativado e reinstale as dependências:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Erro relacionado ao `AdaptaBrasilAPIAccess`

Verifique se o repositório foi clonado na raiz do projeto:

```text
AdaptaBrasil-API---Coleta-e-Consumo-de-Dados/
└── AdaptaBrasilAPIAccess/
```

### Arquivos não foram gerados

Verifique se o programa foi executado a partir da raiz do projeto:

```bash
python main.py
```

O `main.py` deve ser executado com o ambiente virtual ativado.
