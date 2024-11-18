import os
import pandas as pd
import streamlit as st
import plotly.express as px

# Configurações iniciais para o Streamlit
st.set_page_config(layout="wide", page_title="Relatório de Transações")

# Caminho para o arquivo CSV no volume montado
csv_path = "/data/br_cgu_cartao_pagamento_microdados_governo_federal.csv"

# Verificação para garantir que o arquivo foi montado corretamente e existe
if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
    try:
        # Carregar o CSV com cabeçalho
        data = pd.read_csv(csv_path)

        # Converte a coluna 'valor_transacao' para float, ignorando valores não numéricos
        data['valor_transacao'] = pd.to_numeric(data['valor_transacao'], errors='coerce')
        data = data.dropna(subset=['valor_transacao'])

        # Título do Dashboard
        st.title("Relatório de Transações do Governo Federal")

        # Relatório 1: Total de Transações por Ano e Mês
        st.subheader("Total de Transações por Ano e Mês")
        transacoes_ano_mes = data.groupby(['ano_extrato', 'mes_extrato'])['valor_transacao'].sum().reset_index()
        transacoes_ano_mes = transacoes_ano_mes.sort_values(by=['ano_extrato', 'mes_extrato'])
        fig1 = px.bar(transacoes_ano_mes, x='mes_extrato', y='valor_transacao', color='ano_extrato',
                    labels={'valor_transacao': 'Valor Total das Transações', 'mes_extrato': 'Mês', 'ano_extrato': 'Ano'},
                    title="Total de Transações por Ano e Mês")
        st.plotly_chart(fig1)
        
        # Relatório 2: Valor Médio de Transações por Tipo de Transação
        st.subheader("Valor Médio de Transações por Tipo de Transação")
        valor_medio_transacao = data.groupby('transacao')['valor_transacao'].mean().reset_index()
        fig2 = px.bar(valor_medio_transacao, x='transacao', y='valor_transacao',
                      labels={'valor_transacao': 'Valor Médio da Transação', 'transacao': 'Tipo de Transação'},
                      title="Valor Médio das Transações por Tipo de Transação")
        st.plotly_chart(fig2, use_container_width=True)

        # Relatório 3: Top 10 Portadores que Mais Transacionaram
        st.subheader("Top 10 Portadores que Mais Transacionaram")
        top_portadores = data.groupby(['cpf_portador', 'nome_portador'])['valor_transacao'].sum().nlargest(10).reset_index()
        fig3 = px.bar(top_portadores, x='nome_portador', y='valor_transacao',
                      labels={'valor_transacao': 'Valor Total das Transações', 'nome_portador': 'Nome do Portador'},
                      title="Top 10 Portadores por Valor de Transação")
        st.plotly_chart(fig3, use_container_width=True)

        # Relatório 4: Distribuição das Transações por Órgão e Unidade Gestora
        st.subheader("Distribuição das Transações por Órgão e Unidade Gestora")
        transacoes_orgao_unidade = data.groupby(['nome_orgao', 'nome_unidade_gestora'])['valor_transacao'].sum().reset_index()
        fig4 = px.treemap(transacoes_orgao_unidade, path=['nome_orgao', 'nome_unidade_gestora'], values='valor_transacao',
                          title="Distribuição das Transações por Órgão e Unidade Gestora")
        st.plotly_chart(fig4, use_container_width=True)

        # Relatório 5: Distribuição Mensal do Valor de Transações por Órgão Superior
        st.subheader("Distribuição Mensal do Valor de Transações por Órgão Superior")
        distribuicao_orgao_superior = data.groupby(['nome_orgao_superior', 'mes_extrato'])['valor_transacao'].sum().reset_index()
        fig5 = px.line(distribuicao_orgao_superior, x='mes_extrato', y='valor_transacao', color='nome_orgao_superior',
                       labels={'valor_transacao': 'Valor das Transações', 'mes_extrato': 'Mês'},
                       title="Distribuição Mensal das Transações por Órgão Superior")
        st.plotly_chart(fig5, use_container_width=True)

    except pd.errors.EmptyDataError:
        st.write("Erro: O arquivo CSV não contém colunas para serem lidas.")
    except Exception as e:
        st.write(f"Erro ao carregar o arquivo CSV: {e}")
else:
    st.write("Erro: O arquivo CSV não foi encontrado ou está vazio.")
