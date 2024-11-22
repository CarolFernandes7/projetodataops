# Projeto de Data OPS
## Rocket Team (Equipe Rocket)

### Análise de uso com base no "([Cartão de Pagamento do Governo Federal (CPGF)](https://basedosdados.org/dataset/10e96562-3b2a-44e2-b6f9-0472f80993df?table=0e5aff23-79f2-4f52-9c19-bbca1a4232a0))"

## Repositório e arquivos.
Esse repositório utiliza uma base do governo que está localizada dentro de um Atlas do MongoDB, com isso seu acesso é feito via ssh utilizando o MongodbCompass para subir o arquivo e gerenciar o reposítorio localmente na máquina windows.

## app.py

### 1. **Objetivo Principal**
- Carregar dados armazenados em um banco de dados MongoDB Atlas.
- Realizar análises exploratórias e identificar inconsistências nos dados.
- Gerar visualizações interativas para facilitar a compreensão dos padrões e tendências nos dados de transações.

### 2. **Funcionalidades Principais**

#### **Conexão com o MongoDB Atlas**
- O MongoDB é acessado através da biblioteca `pymongo`, utilizando uma URI para conexão segura.
- A conexão é realizada através do usuário `guest:aYQxk4s3RvY9xwMf`, que tem acesso de visualização a todo o banco de dados no mongoDB.
- O banco de dados e a coleção são especificados no código, e os dados são carregados para um DataFrame do Pandas para análise.

#### **Análises de Qualidade de Dados**
- Verificação de valores ausentes e linhas duplicadas.
- Identificação de inconsistências entre códigos e nomes de órgãos.
- Análise de colunas com alta frequência de valores repetidos.

#### **Transformação e Limpeza**
- Conversão de colunas para tipos adequados (`valor_transacao` para numérico e `data_transacao` para datetime).
- Detecção e exibição de outliers no valor das transações utilizando a regra do IQR.

#### **Relatórios e Visualizações**
- **Evolução Temporal**: Linha do tempo dos valores transacionais.
- **Distribuições**:
  - Por órgão e órgão superior.
  - Por faixa de valores transacionais.
- **Análise de Portadores**: Identificação dos principais portadores com maior volume financeiro.
- **Médias e Totais**:
  - Valor médio por tipo de transação.
  - Total de transações agrupadas por ano e mês.

### 3. **Bibliotecas Utilizadas**
- **Streamlit**: Criação da interface interativa.
- **Pandas**: Manipulação de dados tabulares.
- **Plotly**: Geração de gráficos interativos.
- **Pymongo**: Conexão e consulta ao banco de dados MongoDB.

### 4. **Aspectos Técnicos**
- **Configurações do Streamlit**:
  - Layout em tela cheia (`wide`).
  - Título da página definido como "Relatório de Transações".
- **Execuções Seguras**:
  - Uso de `try-except` para evitar falhas em casos de erro ao acessar o banco de dados ou realizar operações nos dados.
  - Verificação da existência e consistência dos dados antes de gerar análises.
- **Estruturação das Visualizações**:
  - Gráficos de barras, linhas e pizza utilizando Plotly para tornar as análises acessíveis e visualmente atraentes.

### 5. **Pontos de Destaque**
- A aplicação inclui verificações e validações robustas para lidar com diferentes estados dos dados, como ausência de registros ou colunas.
- As análises fornecem insights relevantes, como outliers, padrões temporais e inconsistências, facilitando a tomada de decisão.
- O uso de variáveis como `faixa_valor` adiciona um contexto categórico às transações financeiras, permitindo uma análise segmentada.

## docker-compose.yml

1. **Versão**:  
   Define a versão do Docker Compose (`3.8`).

2. **Serviço: streamlit_app**:  
   Configura o contêiner da aplicação Streamlit.
   
   - **build**:  
     Especifica onde está o `Dockerfile` para criar a imagem do contêiner.
       - `context`: O diretório atual (`.`) é usado como contexto de build.
       - `dockerfile`: Nome do arquivo Dockerfile a ser usado.
   
   - **ports**:  
     Mapeia a porta `8501` do contêiner para a porta `8501` da máquina local, permitindo acessar o app via navegador.

   - **volumes**:  
     Monta o diretório local `./app` no contêiner no caminho `/app`, permitindo que alterações no código sejam refletidas sem recriar o contêiner.

   - **environment**:  
     Define variáveis de ambiente usadas pelo Streamlit e pela aplicação:
       - `STREAMLIT_SERVER_ADDRESS=0.0.0.0`: Permite acesso de qualquer IP.
       - `STREAMLIT_SERVER_PORT=8501`: Define a porta usada pelo Streamlit.
       - `STREAMLIT_SERVER_ENABLE_CORS=false`: Desabilita CORS (Cross-Origin Resource Sharing).
       - `MONGO_URI`: Configura a URI para conexão com o banco de dados MongoDB Atlas.

   - **restart**:  
     Garante que o contêiner seja reiniciado automaticamente em caso de falha.

## Dockerfile

1. **Imagem Base**  
   Usamos o Python 3.9 como base:
   ```dockerfile
   FROM python:3.9
   ```

2. **Diretório de Trabalho**  
   Configuramos o diretório `/app` para os arquivos do projeto:
   ```dockerfile
   WORKDIR /app
   ```

3. **Instalação de Dependências**  
   As bibliotecas listadas em `requirements.txt` são instaladas:
   ```dockerfile
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   ```

4. **Arquivo Principal**  
   O arquivo `app.py` é copiado para o contêiner:
   ```dockerfile
   COPY app/app.py .
   ```

5. **Porta e Execução**  
   A porta `8501` é exposta e o Streamlit inicia automaticamente:
   ```dockerfile
   EXPOSE 8501
   CMD ["streamlit", "run", "/app/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false"]
   ```

---

## Requirements

- **streamlit**: Para criar a interface interativa da aplicação.
- **pandas**: Para manipulação e análise de dados.
- **numpy**: Para cálculos numéricos eficientes.
- **plotly**: Para criar gráficos interativos.
- **pymongo**: Para conectar e interagir com o banco de dados MongoDB. 


### Como Usar

1. **Construir a Imagem Docker**  
   ```bash
   docker build -t streamlit-app .
   ```

2. **Executar o Contêiner**  
   ```bash
   docker run -p 8501:8501 streamlit-app
   ```

3. **Acessar o Aplicativo**  
   Abra no navegador:  
   ```
   http://localhost:8501
   ```

---
