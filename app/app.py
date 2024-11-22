import os
import pandas as pd
import streamlit as st
import plotly.express as px
from pymongo import MongoClient

# Configurações iniciais para o Streamlit
st.set_page_config(layout="wide", page_title="Relatório de Transações")

# URL de conexão com o MongoDB Atlas
mongo_uri = "mongodb+srv://guest:aYQxk4s3RvY9xwMf@cluster0.ds4xg.mongodb.net/newbase?retryWrites=true&w=majority"
client = MongoClient(mongo_uri, ssl=True)

# Acessando o banco de dados 'newbase'
db = client["newbase"]  # Nome do banco de dados: "newbase"

# Listar coleções no banco de dados
try:
    colecoes = db.list_collection_names()
    st.write("Coleções disponíveis no banco de dados 'newbase':", colecoes)
except Exception as e:
    st.write(f"Erro ao acessar coleções: {e}")
    st.stop()

# Acessando a coleção 'Base'
collection = db["Base"]

# Verifica o número de documentos na coleção
try:
    count = collection.count_documents({})
    st.write(f"Total de documentos na coleção: {count}")

    if count == 0:
        st.write("A coleção está vazia. Nenhum dado para análise.")
        st.stop()
except Exception as e:
    st.write(f"Erro ao acessar documentos na coleção: {e}")
    st.stop()

# Buscar os dados da coleção
try:
    # Converte os documentos da coleção para um DataFrame
    data = pd.DataFrame(list(collection.find()))

    # Verifica se o DataFrame está vazio
    if data.empty:
        st.write("Erro: Não há dados disponíveis para análise.")
        st.stop()

    # Exibe as primeiras linhas do dataset para inspeção
    st.write("Estrutura do dataset carregado:")
    st.write(data.head())

    # Ajuste de tipos de dados
    if 'valor_transacao' in data.columns:
        data['valor_transacao'] = pd.to_numeric(data['valor_transacao'], errors='coerce')
    if 'data_transacao' in data.columns:
        data['data_transacao'] = pd.to_datetime(data['data_transacao'], errors='coerce')

    # Verificar valores ausentes
    st.title("Análises de Qualidade dos Dados")
    st.subheader("Valores Ausentes por Coluna")
    missing_values = data.isnull().sum()
    st.write(missing_values[missing_values > 0])

    # Linhas duplicadas
    st.subheader("Quantidade de Linhas Duplicadas")
    duplicates = data.duplicated().sum()
    st.write(f"Linhas duplicadas: {duplicates}")

    # Distribuição dos Tipos de Dados
    st.subheader("Tipos de Dados e Inconsistências")
    st.write(data.dtypes)

    # Análise de Outliers em 'valor_transacao'
    st.subheader("Análise de Outliers no Valor das Transações")
    if 'valor_transacao' in data.columns:
        q1 = data['valor_transacao'].quantile(0.25)
        q3 = data['valor_transacao'].quantile(0.75)
        iqr = q3 - q1
        threshold = q3 + 1.5 * iqr
        outliers = data[data['valor_transacao'] > threshold]
        st.write(f"Quantidade de Outliers: {outliers.shape[0]}")
        st.write(outliers[['valor_transacao', 'nome_portador']].head())

    # Consistência nas Hierarquias
    st.subheader("Consistência entre Códigos e Nomes de Órgãos")
    if 'codigo_orgao' in data.columns and 'nome_orgao' in data.columns:
        inconsistencias = data.groupby('codigo_orgao')['nome_orgao'].nunique()
        inconsistencias = inconsistencias[inconsistencias > 1]
        st.write("Órgãos com inconsistências:")
        st.write(inconsistencias)

    # Colunas com Alta Frequência de Valores Repetidos
    st.subheader("Colunas com Alta Frequência de Valores Repetidos")
    repeated_columns = {
        col: data[col].value_counts(normalize=True).max()
        for col in data.columns
        if data[col].value_counts(normalize=True).max() > 0.9
    }
    st.write(repeated_columns)


    st.title("Relatórios e Visualizações")

    # Total de Transações por Ano e Mês
    st.subheader("Total de Transações por Ano e Mês")
    if 'ano_extrato' in data.columns and 'mes_extrato' in data.columns:
        transacoes_ano_mes = (
            data.groupby(['ano_extrato', 'mes_extrato'])['valor_transacao']
            .sum()
            .reset_index()
        )
        fig1 = px.bar(
            transacoes_ano_mes,
            x='mes_extrato',
            y='valor_transacao',
            color='ano_extrato',
            title="Total de Transações por Ano e Mês"
        )
        st.plotly_chart(fig1, use_container_width=True)

    # Valor Médio de Transações por Tipo
    st.subheader("Valor Médio por Tipo de Transação")
    if 'transacao' in data.columns:
        valor_medio_transacao = (
            data.groupby('transacao')['valor_transacao']
            .mean()
            .reset_index()
        )
        fig2 = px.bar(
            valor_medio_transacao,
            x='transacao',
            y='valor_transacao',
            title="Valor Médio por Tipo de Transação"
        )
        st.plotly_chart(fig2, use_container_width=True)


    # Distribuição de Transações por Órgão
    st.subheader("Distribuição de Transações por Órgão")
    if 'nome_orgao' in data.columns:
        transacoes_por_orgao = (
            data.groupby('nome_orgao')['valor_transacao']
            .sum()
            .reset_index()
            .sort_values(by='valor_transacao', ascending=False)
        )
        fig7 = px.bar(
            transacoes_por_orgao,
            x='nome_orgao',
            y='valor_transacao',
            title="Distribuição de Transações por Órgão",
            labels={'valor_transacao': 'Valor Total (R$)', 'nome_orgao': 'Órgão'},
        )
        st.plotly_chart(fig7, use_container_width=True)

    # Distribuição de Transações por Órgão Superior
    st.subheader("Distribuição de Transações por Órgão Superior")
    if 'nome_orgao_superior' in data.columns:
        transacoes_por_orgao_superior = (
            data.groupby('nome_orgao_superior')['valor_transacao']
            .sum()
            .reset_index()
            .sort_values(by='valor_transacao', ascending=False)
        )
        fig8 = px.pie(
            transacoes_por_orgao_superior,
            names='nome_orgao_superior',
            values='valor_transacao',
            title="Distribuição de Transações por Órgão Superior",
            hole=0.4,
        )
        st.plotly_chart(fig8, use_container_width=True)

    # Análise de Portadores (Top 10)
    st.subheader("Top 10 Portadores com Maior Valor de Transações")
    if 'cpf_portador' in data.columns and 'nome_portador' in data.columns:
        top_portadores = (
            data.groupby(['cpf_portador', 'nome_portador'])['valor_transacao']
            .sum()
            .nlargest(10)
            .reset_index()
        )
        fig9 = px.bar(
            top_portadores,
            x='nome_portador',
            y='valor_transacao',
            color='cpf_portador',
            title="Top 10 Portadores por Valor de Transação",
            labels={
                'nome_portador': 'Portador',
                'valor_transacao': 'Valor Total (R$)',
                'cpf_portador': 'CPF do Portador',
            },
        )
        st.plotly_chart(fig9, use_container_width=True)

    # Análise Temporal de Transações
    st.subheader("Análise Temporal de Transações")
    if 'data_transacao' in data.columns:
        transacoes_temporal = (
            data.groupby('data_transacao')['valor_transacao']
            .sum()
            .reset_index()
        )
        fig11 = px.line(
            transacoes_temporal,
            x='data_transacao',
            y='valor_transacao',
            title="Evolução Temporal do Valor de Transações",
            labels={
                'data_transacao': 'Data',
                'valor_transacao': 'Valor Total (R$)',
            },
        )
        st.plotly_chart(fig11, use_container_width=True)

    # Transações por Faixa de Valores
    st.subheader("Distribuição de Transações por Faixa de Valores")
    if 'valor_transacao' in data.columns:
        bins = [0, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]
        labels = [
            "Até R$1.000",
            "R$1.000 - R$5.000",
            "R$5.000 - R$10.000",
            "R$10.000 - R$50.000",
            "R$50.000 - R$100.000",
            "R$100.000 - R$500.000",
            "Acima de R$500.000",
        ]
        data['faixa_valor'] = pd.cut(data['valor_transacao'], bins=bins, labels=labels, right=False)
        transacoes_faixa = (
            data.groupby('faixa_valor')['valor_transacao']
            .sum()
            .reset_index()
        )
        fig12 = px.bar(
            transacoes_faixa,
            x='faixa_valor',
            y='valor_transacao',
            title="Distribuição de Transações por Faixa de Valores",
            labels={
                'faixa_valor': 'Faixa de Valores',
                'valor_transacao': 'Valor Total (R$)',
            },
        )
        st.plotly_chart(fig12, use_container_width=True)

except Exception as e:
    st.write(f"Erro durante o processamento dos dados: {e}")