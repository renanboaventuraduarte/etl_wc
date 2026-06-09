import pandas as pd
from sqlalchemy import create_engine
import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

# CONFIGURAÇÃO DO GEMINI
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODELO = "gemini-2.5-flash"

# Definições do AWS RDS
USER = 'postgres'  # O usuário do banco de dados
PASSWORD = 'FIQmwPFmX5U2Ijtcwoax'  # A senha do banco de dados
# O endpoint do banco de dados
HOST = 'etlwc.cpe22c8qab2g.us-east-2.rds.amazonaws.com'
PORT = 5432  # Porta padrão do PostgreSQL
DATABASE = 'postgres'  # O nome do banco de dados

# EXTRAÇÃO E TRANSFORMAÇÃO
data_raw = r'C:\Users\Gamer\Desktop\Engenharia de dados\Cursos\Desafio_ETL\ETL_World_Cup\db_wc\world_cups.csv'
df = pd.read_csv(data_raw)

winners = df['Winner'].value_counts().rename('winners')
seconds = df['Second'].value_counts().rename('second')
thirds = df['Third'].value_counts().rename('third')

table = pd.concat([winners, seconds, thirds], axis=1).fillna(0).astype(int)
table['somatoria_top_3'] = table['winners'] + \
    table['second'] + table['third']
table = table.reset_index().rename(columns={'index': 'nome_do_pais'})
table = table.sort_values(by='somatoria_top_3', ascending=False)

# FUNÇÃO PARA CONECTAR AO GEMINI (Linha por Linha)


def obter_curiosidade_pais(pais):
    """Função que consulta o Gemini para um país específico."""
    print(
        # Log para acompanhar o progresso no terminal
        f"Buscando curiosidade para: {pais}...")
    try:
        prompt = (
            f"Escreva apenas uma curiosidade histórica, curta e impactante (máximo 2 frases), "
            f"sobre a seleção de futebol do(a) {pais} em Copas do Mundo."
        )

        response = client.models.generate_content(
            model=MODELO,
            contents=prompt
        )

        time.sleep(4.5)

        return response.text.strip()
    except Exception as e:
        if "429" in str(e):
            print(f"Cota atingida para {pais}. Aguardando janela de tempo...")
            time.sleep(7)
            try:
                response = client.models.generate_content(
                    model=MODELO, contents=prompt)
                return response.text.strip()
            except Exception:
                return "Curiosidade temporariamente indisponível por limite de acessos."

        print(f"Erro inesperado para {pais}: {e}")
        return "Curiosidade não disponível no momento."


# Preenche a coluna para cada país
table['curiosidade'] = table['nome_do_pais'].apply(obter_curiosidade_pais)

# CARREGAMENTO (Conexão direta via Usuário e Senha)
string_connection = f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?sslmode=require'
engine = create_engine(string_connection)

# Envio do DataFrame para o AWS RDS
table.to_sql(
    name='ranking_top_3_copas',
    con=engine,
    if_exists='replace',
    index=False
)

print("Dados enviados com sucesso para a tabela 'ranking_top_3_copas' no AWS RDS (via Usuário/Senha)!")
