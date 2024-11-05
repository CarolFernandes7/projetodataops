import pandas as pd
from sqlalchemy import create_engine

# Carregar o arquivo CSV para um DataFrame
try:
    df = pd.read_csv('basegoverno.csv')
    print("Dados carregados no DataFrame:")
    print(df.head())  # Exibir as primeiras linhas para verificar
except FileNotFoundError:
    print("Erro: Arquivo 'basegoverno.csv' não encontrado. Verifique o caminho e tente novamente.")
    exit()

# Configuração da conexão com PostgreSQL local
user = 'carol_user'
password = '12345678'
host = 'localhost'           # Usando localhost para banco local
port = '5432'                # Porta padrão do PostgreSQL
database = 'basegoverno'     # Nome do seu banco de dados

# Criação da string de conexão
connection_string = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'

# Teste de conexão com o banco de dados
try:
    engine = create_engine(connection_string)
    connection = engine.connect()
    print("Conexão com o banco de dados bem-sucedida!")
    connection.close()
except Exception as e:
    print("Erro na conexão com o banco de dados:", e)
    exit()

# Nome da tabela de destino no banco de dados
table_name = 'tabela_basegoverno'  # Substitua pelo nome desejado da tabela

# Enviar o DataFrame para o banco de dados
try:
    df.to_sql(table_name, engine, index=False, if_exists='replace')
    print("Dados carregados com sucesso no banco de dados!")
except Exception as e:
    print("Ocorreu um erro ao carregar os dados:", e)