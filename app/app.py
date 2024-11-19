import os
import pandas as pd
import streamlit as st
import plotly.express as px
from pymongo import MongoClient

# Configurações iniciais para o Streamlit
st.set_page_config(layout="wide", page_title="Relatório de Transações")

# URL de conexão com o MongoDB Atlas
mongo_uri = "mongodb+srv://ahylm09x2:4KabHKiKXRLQqXhT@cluster0.ds4xg.mongodb.net/newbase?retryWrites=true&w=majority"
client = MongoClient(mongo_uri, ssl=True)

# Acessando o banco de dados 'newbase'
db = client["newbase"]  # Nome do banco de dados: "newbase"

# Listar coleções no banco de dados 'newbase'
colecoes = db.list_collection_names()
st.write("Coleções disponíveis no banco de dados 'newbase':", colecoes)

# Acessando a coleção 'Base'
collection = db["Base"]  # Nome da coleção: "Base"

# Verifica o número de documentos na coleção
count = collection.count_documents({})
st.write(f"Total de documentos na coleção: {count}")

# Caso a coleção esteja vazia
if count == 0:
    st.write("Erro: A coleção está vazia.")

# Buscar os dados da coleção
try:
    # Converte os documentos da coleção para um DataFrame
    data = pd.DataFrame(list(collection.find()))
    
    # Verifica se os dados foram carregados
    if data.empty:
        st.write("Erro: Não há dados na coleção.")
    else:
        # Exibe as primeiras linhas do dataset para inspeção
        st.write("Estrutura do dataset carregado:")
        st.write(data.head())

        # Converte a coluna 'valor_transacao' para float
        if 'valor_transacao' in data.columns:
            data['valor_transacao'] = pd.to_numeric(data['valor_transacao'], errors='coerce')
            data = data.dropna(subset=['valor_transacao'])  # Remove valores nulos

            # Relatório 1: Total de Transações por Ano e Mês
            st.title("Relatório de Transações - Base de Dados")
            st.subheader("Total de Transações por Ano e Mês")
            if 'ano_extrato' in data.columns and 'mes_extrato' in data.columns:
                transacoes_ano_mes = data.groupby(['ano_extrato', 'mes_extrato'])['valor_transacao'].sum().reset_index()
                transacoes_ano_mes = transacoes_ano_mes.sort_values(by=['ano_extrato', 'mes_extrato'])
                fig1 = px.bar(
                    transacoes_ano_mes,
                    x='mes_extrato',
                    y='valor_transacao',
                    color='ano_extrato',
                    labels={
                        'valor_transacao': 'Valor Total das Transações',
                        'mes_extrato': 'Mês',
                        'ano_extrato': 'Ano',
                    },
                    title="Total de Transações por Ano e Mês"
                )
                st.plotly_chart(fig1)

            # Relatório 2: Valor Médio de Transações por Tipo de Transação
            st.subheader("Valor Médio de Transações por Tipo de Transação")
            if 'transacao' in data.columns:
                valor_medio_transacao = data.groupby('transacao')['valor_transacao'].mean().reset_index()
                fig2 = px.bar(
                    valor_medio_transacao,
                    x='transacao',
                    y='valor_transacao',
                    labels={
                        'valor_transacao': 'Valor Médio da Transação',
                        'transacao': 'Tipo de Transação',
                    },
                    title="Valor Médio das Transações por Tipo de Transação"
                )
                st.plotly_chart(fig2, use_container_width=True)

            # Relatório 3: Top 10 Portadores que Mais Transacionaram
            st.subheader("Top 10 Portadores que Mais Transacionaram")
            if 'cpf_portador' in data.columns and 'nome_portador' in data.columns:
                top_portadores = data.groupby(['cpf_portador', 'nome_portador'])['valor_transacao'].sum().nlargest(10).reset_index()
                fig3 = px.bar(
                    top_portadores,
                    x='nome_portador',
                    y='valor_transacao',
                    labels={
                        'valor_transacao': 'Valor Total das Transações',
                        'nome_portador': 'Nome do Portador',
                    },
                    title="Top 10 Portadores por Valor de Transação"
                )
                st.plotly_chart(fig3, use_container_width=True)

            # Relatório 4: Distribuição das Transações por Órgão e Unidade Gestora
            st.subheader("Distribuição das Transações por Órgão e Unidade Gestora")
            if 'nome_orgao' in data.columns and 'nome_unidade_gestora' in data.columns:
                transacoes_orgao_unidade = data.groupby(['nome_orgao', 'nome_unidade_gestora'])['valor_transacao'].sum().reset_index()
                fig4 = px.treemap(
                    transacoes_orgao_unidade,
                    path=['nome_orgao', 'nome_unidade_gestora'],
                    values='valor_transacao',
                    title="Distribuição das Transações por Órgão e Unidade Gestora"
                )
                st.plotly_chart(fig4, use_container_width=True)

            # Relatório 5: Distribuição Mensal do Valor de Transações por Órgão Superior
            st.subheader("Distribuição Mensal do Valor de Transações por Órgão Superior")
            if 'nome_orgao_superior' in data.columns:
                distribuicao_orgao_superior = data.groupby(['nome_orgao_superior', 'mes_extrato'])['valor_transacao'].sum().reset_index()
                fig5 = px.line(
                    distribuicao_orgao_superior,
                    x='mes_extrato',
                    y='valor_transacao',
                    color='nome_orgao_superior',
                    labels={'valor_transacao': 'Valor das Transações', 'mes_extrato': 'Mês'},
                    title="Distribuição Mensal das Transações por Órgão Superior"
                )
                st.plotly_chart(fig5, use_container_width=True)

except Exception as e:
    st.write(f"Erro ao conectar ao MongoDB ou carregar os dados: {e}")