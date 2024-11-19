from pymongo import MongoClient

# Substitua pela sua string de conexão
uri = "mongodb+srv://ahylm09x2:4KabHKiKXRLQqXhT@cluster0.ds4xg.mongodb.net/newbase?retryWrites=true&w=majority"

try:
    # Cria o cliente MongoDB
    client = MongoClient(uri)
    
    # Testa a conexão acessando um banco de dados
    db = client.get_database("newbase")
    print("Conexão bem-sucedida ao banco de dados!")
except Exception as e:
    print("Erro ao conectar ao MongoDB:", e)
