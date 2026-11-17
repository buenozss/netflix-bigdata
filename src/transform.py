
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    split,
    trim,
    when,
    to_date,
    regexp_extract,
    struct,
    lit
)
from pyspark.sql.types import IntegerType


def transformar_dados():

    # Iniciar a sessão do Spark
    spark = SparkSession.builder \
        .appName("NetflixBigData") \
        .master("local[*]") \
        .config("spark.sql.ansi.enabled", "false") \
        .getOrCreate()

    # Ler o arquivo CSV como texto
    df = spark.read.csv(
        "data/raw/netflix_titles.csv",
        header=True,
        inferSchema=False
    )

    # Remover espaços desnecessários dos textos
    for coluna in df.columns:
        df = df.withColumn(coluna, trim(col(coluna)))

    # Converter valores vazios em NULL
    df = df.na.replace("", None)

    # Converter o ano de lançamento para inteiro
    df = df.withColumn(
        "release_year",
        col("release_year").cast(IntegerType())
    )

    # Converter a data para o formato Date
    df = df.withColumn(
        "date_added",
        to_date(col("date_added"), "MMMM d, yyyy")
    )

    # Transformar campos separados por vírgula em listas
    colunas_lista = ["director", "cast", "country", "listed_in"]

    for coluna in colunas_lista:
        df = df.withColumn(
            coluna,
            when(
                col(coluna).isNotNull(),
                split(col(coluna), ",\\s*")
            ).otherwise(None)
        )

    # Extrair o valor numérico da duração
    valor_duracao = regexp_extract(
        col("duration"),
        r"(\d+)",
        1
    ).cast(IntegerType())

    # Identificar a unidade da duração
    unidade_duracao = when(
        col("duration").contains("Season"),
        lit("seasons")
    ).otherwise(lit("minutes"))

    # Criar estrutura com valor e unidade
    df = df.withColumn(
        "duration",
        when(
            col("duration").isNotNull(),
            struct(
                valor_duracao.alias("value"),
                unidade_duracao.alias("unit")
            )
        ).otherwise(None)
    )

    # Mostrar os primeiros registros
    df.show(5, truncate=False)

    # Exibir a estrutura dos dados
    df.printSchema()

    # Salvar os dados transformados em formato Parquet
    df.write.mode("overwrite").parquet("data/processed/netflix")

    print("Dados salvos em Parquet com sucesso!")

    return df
