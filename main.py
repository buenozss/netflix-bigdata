from src.transform import transformar_dados
from src.load_mongodb import carregar_mongodb

print("Iniciando pipeline Netflix...")

# Etapa 1: Transformar os dados com Spark
df = transformar_dados()

# Etapa 2: Carregar os dados no MongoDB
carregar_mongodb()

print("Pipeline executado com sucesso!")