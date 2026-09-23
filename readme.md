# AdaptaBrasil API — Coleta e Consumo de Dados

Projeto para automatizar a coleta e o consumo de dados da API do **AdaptaBrasil**, organizando os resultados em arquivos CSV por setor, indicador e tipo de desastre.

## Fluxo do projeto

O processamento é dividido em duas etapas:

1. **`API/coleta_dados.py`**

   * Lê a estrutura de indicadores do AdaptaBrasil.
   * Filtra os indicadores relevantes.
   * Gera os arquivos de apoio em `API/Data`.

2. **`API/consumo_api.py`**

   * Lê os indicadores filtrados.
   * Consulta os endpoints da API.
   * Salva os resultados em `API/output`, separados por categoria.

Exemplos de categorias:

```text
API/output/
├── Deslizamento de terra/
├── Inundações, enxurradas e alagamentos/
└── Risco de estresse hídrico/
```

## Estrutura

```text
api fagner/
├── AdaptaBrasilAPIAccess/
│   ├── AdaptaBrasilAPIAccess.py
│   ├── adaptaBrasilAPIEstrutura.csv
│   └── requirements.txt
├── API/
│   ├── Data/
│   ├── output/
│   ├── coleta_dados.py
│   └── consumo_api.py
├── requirements.txt
├── readme.md
└── output.json
```

## Pré-requisitos

* Python 3.9+
* Git
* Acesso à internet

## Instalação

### 1. Clone o projeto `AdaptaBrasilAPIAccess`

Na raiz do projeto, clone o repositório oficial:

```powershell
git clone https://github.com/AdaptaBrasil/AdaptaBrasilAPIAccess.git
```

O diretório `AdaptaBrasilAPIAccess` deve ficar na raiz do projeto:

```text
api fagner/
├── AdaptaBrasilAPIAccess/
└── API/
```

### 2. Crie o ambiente virtual

No diretório raiz:

```powershell
python -m venv .venv
```

Ative o ambiente no PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Caso o PowerShell bloqueie a execução:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Caso necessário, as dependências principais são:

```powershell
pip install pandas requests
```

## Execução

Os scripts devem ser executados nesta ordem.

### 1. Preparar os indicadores

```powershell
python .\API\coleta_dados.py
```

Esse comando gera os arquivos em:

```text
API/Data/
├── adaptaBrasilAPIEstrutura.csv
├── sectoral_risk.csv
└── GeoHydrological_Disasters.csv
```

### 2. Consumir os dados da API

```powershell
python .\API\consumo_api.py
```

Os resultados serão salvos em:

```text
API/output/
```

## Execução rápida

Depois de clonar o projeto e o `AdaptaBrasilAPIAccess`, basta:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python .\API\coleta_dados.py
python .\API\consumo_api.py
```

## Problemas comuns

**Erro ao ativar o ambiente virtual:**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**`ModuleNotFoundError`:**

```powershell
pip install -r requirements.txt
```

**Arquivos não encontrados ou não gerados:**

Verifique se o `AdaptaBrasilAPIAccess` foi clonado na raiz do projeto e se os scripts foram executados na ordem:

```text
coleta_dados.py → consumo_api.py
```
