# 🏆 Pipeline de ETL: Copa do Mundo & Inteligência Artificial (Gemini API)

Este é um projeto prático de **Engenharia de Dados** desenvolvido como parte do módulo "Desafio ETL". O objetivo principal é extrair dados históricos das Copas do Mundo de Futebol, transformar e consolidar estatísticas das melhores seleções (Top 3), enriquecer o relatório final consumindo dados dinamicamente através da API do Google Gemini e distribuí-los em múltiplos destinos de armazenamento (Multi-Target Load).

---

## 📌 Arquitetura do Pipeline (ETL)

O projeto segue a arquitetura clássica de um pipeline de dados, implementando uma estratégia de escrita multi-destino (Local, On-Premise e Cloud):

1.  **Extract (Extração):** Leitura de dados brutos históricos a partir de um arquivo CSV local utilizando a biblioteca **Pandas**.
2.  **Transform (Transformação):**
    * Agrupamento e contagem de colocações (1º, 2º e 3º lugar) por país.
    * Consolidação das métricas através de concatenação e tratamento de valores nulos (`.fillna(0)`).
    * Criação de uma métrica personalizada (`somatoria_top_3`) e ordenação do ranking.
    * **Enriquecimento com IA:** Integração com o modelo `gemini-2.5-flash` utilizando o **Google GenAI SDK** para gerar de forma automatizada uma curiosidade histórica única para cada país da tabela.
3.  **Load (Carregamento Multicamadas):**
    * **Local File System:** Geração de um arquivo flat estruturado (`ranking_top_3_copas.csv`) para análises rápidas em ferramentas locais.
    * **On-Premise (PostgreSQL Local):** Carga dos dados estruturados em uma instância local do banco de dados PostgreSQL para persistência relacional.
    * **Cloud (Amazon RDS):** Persistência de produção em uma instância gerenciada de PostgreSQL na nuvem da AWS (Amazon Relational Database Service), simulando um ambiente real de data warehouse/analytics pronto para ferramentas de BI na nuvem (como Power BI Service ou Looker Studio).

---

## 🛠️ Tecnologias e Ferramentas

* **Python 3.13** (Linguagem de programação principal)
* **Pandas** (Manipulação e análise de dados)
* **SQLAlchemy & Psycopg2** (Engine e driver de conexão de dados para os bancos PostgreSQL)
* **Google GenAI SDK (`google-genai`)** (Consumo do modelo de linguagem `gemini-2.5-flash`)
* **Amazon RDS (PostgreSQL)** (Banco de dados relacional gerenciado na Nuvem AWS)
* **PostgreSQL Local** (Banco de dados relacional para ambiente de desenvolvimento)
* **Python-Dotenv** (Gerenciamento seguro de credenciais e variáveis de ambiente)
* **Time (Biblioteca nativa)** (Mecanismo de controle de concorrência/ritmo)

---

## 🚀 Desafios Técnicos Superados: Engenharia vs APIs Externas

Durante o desenvolvimento deste pipeline, um cenário real de produção foi enfrentado e mitigado: **O estouro de limites de requisição (Rate Limiting - Erro `429 RESOURCE_EXHAUSTED`)**.

Como a API do Gemini na camada gratuita possui um limite estrito de **15 requisições por minuto (RPM)**, a execução direta do Pandas `.apply()` sobrecarregava o servidor instantaneamente.

### Soluções de Engenharia Aplicadas:
* **Throttling / Rate Limiting Manual:** Implementação de uma pausa estratégica (`time.sleep(4.5)`) entre o processamento de cada linha. Isso garante que o pipeline execute no ritmo exato aceito pela API.
* **Mecanismo de Retry (Backoff):** Inclusão de um bloco `try-except` especializado em capturar o erro `429`. Caso a API sofra oscilações ou atinja a cota, o pipeline aguarda 7 segundos para a janela de tempo resetar e tenta reprocessar o registro automaticamente, evitando a quebra do processo.
* **Segurança da Informação:** Credenciais de acesso locais e de nuvem (AWS), além das chaves de API, gerenciadas estritamente via variáveis de ambiente (`.env`), impedindo o vazamento de chaves no controle de versão (Git).

---

## 📋 Como Executar o Projeto

### 1. Clonar o Repositório
```bash
git clone [https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git)
cd NOME_DO_REPOSITORIO
```

### 2. Configurar o Ambiente Virtual e Dependências
```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente (Windows)
.\venv\Scripts\activate

# Instalar as bibliotecas necessárias
pip install pandas google-genai sqlalchemy psycopg2-binary python-dotenv
```

### 3. Configurar as Variáveis de Ambiente
Crie um arquivo chamado .env na raiz do projeto para armazenar os endpoints e dados de conexão de forma segura:

Snippet de código
# API Key do Gemini
GEMINI_API_KEY=seu_token_do_gemini_aqui

# Banco de Dados Local (PostgreSQL)
LOCAL_DB_HOST=localhost
LOCAL_DB_PORT=5432
LOCAL_DB_NAME=seu_banco_local
LOCAL_DB_USER=seu_usuario_local
LOCAL_DB_PASS=sua_senha_local

# Banco de Dados Cloud (Amazon RDS PostgreSQL)
RDS_DB_HOST=seu-endpoint-rds.amazonaws.com
RDS_DB_PORT=5432
RDS_DB_NAME=seu_banco_rds
RDS_DB_USER=seu_usuario_rds
RDS_DB_PASS=sua_senha_rds

### 4. Execução do Pipeline
Execute o script principal:

```bash
python ETL_World_Cup/etl_wc_local_ia.py
```

📂 Estrutura do Repositório
Plaintext

```
.
├── ETL_World_Cup/
│   ├── db_wc/
│   │   └── world_cups.csv          # Base de dados bruta (Extract)
│   └── etl_wc_db_ia.py             # Script principal Python (ETL On-Premise, PostgreSQL)
|   └── etl_wc_ia.py                # Script principal Python (ETL Cloud, Amazon RDS)
|   └── etl_wc_local_ia.py          # Script principal Python (ETL Local File System)
├── .env.example                    # Modelo para configuração das chaves de conexão
├── .gitignore                      # Proteção para ignorar .env e venv/
├── ranking_top_3_copas.csv         # Destino 1: Arquivo final gerado (Local Load)
└── README.md                       # Documentação do projeto
```
