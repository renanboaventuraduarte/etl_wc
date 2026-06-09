# 🏆 Pipeline de ETL: Copa do Mundo & Inteligência Artificial (Gemini API)

Este é um projeto de estudo prático focado em **Engenharia de Dados**, desenvolvido como parte do módulo "Desafio ETL". O objetivo principal é extrair dados históricos das Copas do Mundo de Futebol, transformar e consolidar estatísticas das melhores seleções (Top 3) e enriquecer o relatório final consumindo dados de forma dinâmica através da API do Google Gemini.

## 📌 Arquitetura do Pipeline (ETL)

O projeto segue a arquitetura clássica de um pipeline de dados:

1.  **Extract (Extração):** Leitura de dados brutos históricos a partir de um arquivo local (`world_cups.csv`) utilizando a biblioteca **Pandas**.
2.  **Transform (Transformação):**
    * Agrupamento e contagem de colocações (1º, 2º e 3º lugar) por país.
    * Consolidação das métricas através de concatenação e tratamento de valores nulos (`.fillna(0)`).
    * Criação de uma métrica personalizada (`somatoria_top_3`) e ordenação do ranking.
    * **Enriquecimento com IA:** Integração com o modelo `gemini-2.5-flash` utilizando o novo **Google GenAI SDK** para gerar de forma automatizada uma curiosidade histórica única para cada país da tabela.
3.  **Load (Carregamento):** Exportação dos dados transformados e enriquecidos para um novo arquivo estruturado (`ranking_top_3_copas.csv`) pronto para consumo por ferramentas de Analytics ou BI.

---

## 🛠️ Tecnologias e Ferramentas

* **Python 3.13** (Linguagem de programação principal)
* **Pandas** (Manipulação e análise de dados)
* **Google GenAI SDK (`google-genai`)** (Consumo do modelo de linguagem `gemini-2.5-flash`)
* **Time (Biblioteca nativa)** (Mecanismo de controle de concorrência/ritmo)

---

## 🚀 Desafios Técnicos Superados: Engenharia vs APIs Externas

Durante o desenvolvimento deste pipeline, um cenário real de engenharia de dados foi enfrentado e mitigado: **O estouro de limites de requisição (Rate Limiting - Erro `429 RESOURCE_EXHAUSTED`)**.

Como a API do Gemini na camada gratuita possui um limite estrito de **15 requisições por minuto (RPM)**, a execução direta do Pandas `.apply()` sobrecarregava o servidor da Google instantaneamente.

### Soluções de Engenharia Aplicadas:
* **Throttling / Rate Limiting Manual:** Implementação de uma pausa estratégica (`time.sleep(4.5)`) entre o processamento de cada linha. Isso garante que o pipeline execute no ritmo exato aceito pela API (máximo de 13 requisições por minuto).
* **Mecanismo de Retry (Backoff):** Inclusão de um bloco `try-except` especializado em capturar o erro `429`. Caso a API sofra oscilações ou atinja a cota, o pipeline aguarda 7 segundos para a janela de tempo resetar e tenta reprocessar o registro automaticamente, evitando a quebra do pipeline em produção.

---

## 📋 Como Executar o Projeto

### 1. Pré-requisitos
Certifique-se de ter o Python instalado e suas dependências atualizadas. É recomendado o uso de um ambiente virtual (`venv`).

Instale as bibliotecas necessárias:
```bash
pip install pandas google-genai
