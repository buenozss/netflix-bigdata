
import os
import json

from dotenv import load_dotenv
from pymongo import MongoClient
from pyspark.sql import SparkSession


def carregar_mongodb():

    # Carregar as variáveis do arquivo .env
    load_dotenv()

    uri = os.getenv("MONGODB_URI")

    if not uri:
        raise ValueError("MONGODB_URI não encontrada no arquivo .env")

    client = None
    spark = None

    try:
        # Conectar ao MongoDB
        client = MongoClient(uri, serverSelectionTimeoutMS=10000)

        # Verificar a conexão
        client.admin.command("ping")
        print("Conexão com MongoDB realizada com sucesso!")

        # Selecionar o banco de dados e a coleção
        banco = client["netflix"]
        colecao = banco["netflix_titles"]

        # Iniciar ou reutilizar a sessão do Spark
        spark = SparkSession.builder \
            .appName("NetflixMongoDB") \
            .master("local[*]") \
            .getOrCreate()

        # Ler os dados transformados em Parquet
        df = spark.read.parquet("data/processed/netflix")

        # Converter os dados do Spark para uma lista de documentos Python
        documentos = [
            json.loads(linha)
            for linha in df.toJSON().collect()
        ]

        if not documentos:
            raise ValueError("Nenhum documento encontrado para inserir.")

        # Limpar a coleção para evitar registros duplicados
        colecao.delete_many({})

        # Inserir os documentos no MongoDB
        resultado = colecao.insert_many(documentos)

        print(f"{len(resultado.inserted_ids)} documentos enviados ao MongoDB!")
        print(f"Total de documentos na coleção: {colecao.count_documents({})}")

    finally:
        # Encerrar as conexões
        if client:
            client.close()

        if spark:
            spark.stop()
