import os
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# Carregar o arquivo CSV completo
try:
    df = pd.read_csv('basegoverno.csv')
    print("Dados carregados no DataFrame com sucesso.")
    print(df.head())  # Exibir as primeiras linhas para verificar
except FileNotFoundError:
    print("Erro: Arquivo 'basegoverno.csv' não encontrado. Verifique o caminho e tente novamente.")
    exit()

# Filtrar dados dos últimos 10 anos
ano_atual = datetime.now().year
ano_limite = ano_atual - 10

# Supondo que a coluna de ano é 'ano_extrato'
try:
    df_filtrado = df[df['ano_extrato'] >= ano_limite]
    print("Dados filtrados para os últimos 10 anos com sucesso.")
    print(df_filtrado.head())
except KeyError:
    print("Erro: Coluna 'ano_extrato' não encontrada no arquivo CSV. Verifique o arquivo.")
    exit()

# Salvar o DataFrame filtrado em um novo arquivo CSV
try:
    df_filtrado.to_csv('basegoverno_filtrado.csv', index=False)
    print("Arquivo 'basegoverno_filtrado.csv' salvo com sucesso.")
except Exception as e:
    print("Erro ao salvar o arquivo filtrado:", e)
    exit()

# Verificar se o arquivo foi criado
if os.path.exists('basegoverno_filtrado.csv'):
    print("Confirmação: o arquivo 'basegoverno_filtrado.csv' foi criado.")
else:
    print("Erro: o arquivo 'basegoverno_filtrado.csv' não foi criado.")
    exit()

# Configuração da conexão com PostgreSQL local
user = 'carol_user'
password = '12345678'
host = 'localhost'
port = '5432'
database = 'basegoverno'

# Criação da string de conexão
connection_string = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
engine = create_engine(connection_string)

# Nome da tabela de destino no banco de dados
table_name = 'tabela_basegoverno_filtrado'

# Enviar o DataFrame filtrado para o banco de dados
try:
    print("Iniciando o envio dos dados filtrados para o banco de dados...")
    df_filtrado.to_sql(table_name, engine, index=False, if_exists='replace')
    print("Dados filtrados carregados com sucesso no banco de dados!")
except Exception as e:
    print("Ocorreu um erro ao carregar os dados filtrados no banco de dados:", e)