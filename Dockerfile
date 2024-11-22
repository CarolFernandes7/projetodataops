# Use a imagem base do Python
FROM python:3.9

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar o arquivo requirements.txt para o contêiner e instalar as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o arquivo app.py
COPY app/app.py .

# Expor a porta usada pelo Streamlit
EXPOSE 8501

# Comando para rodar o Streamlit apontando para o app.py
CMD ["streamlit", "run", "/app/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false"]
