
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGODB_URI")

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=10000)
    client.admin.command("ping")

    print("Conexão com MongoDB realizada com sucesso!")

    client.close()

except Exception as erro:
    print("Erro ao conectar:", erro)
