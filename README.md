
# Pipeline Big Data - Netflix

## Sobre o projeto

Este projeto implementa um pipeline de ingestão e processamento de Big Data utilizando o conjunto de dados Netflix Movies and TV Shows.

O objetivo é realizar a leitura, transformação e armazenamento dos dados em um banco de dados NoSQL, utilizando Apache Spark e MongoDB.

## Tecnologias utilizadas

- Python
- Apache Spark (PySpark)
- MongoDB Atlas
- Pandas
- Parquet
- KaggleHub

## Fluxo do pipeline

1. **Ingestão:** download do conjunto de dados Netflix por meio do KaggleHub.
2. **Leitura:** leitura do arquivo CSV utilizando Apache Spark.
3. **Transformação:** limpeza dos dados, tratamento de valores nulos e conversão dos campos.
4. **Armazenamento intermediário:** gravação dos dados processados no formato Parquet.
5. **Carga:** envio dos documentos para o MongoDB Atlas.

## Estrutura do projeto

```text
netflix-bigdata/
├── data/
│   ├── raw/
│   │   └── netflix_titles.csv
│   └── processed/
│       └── netflix/
├── src/
│   ├── transform.py
│   ├── load_mongodb.py
│   └── test_connection.py
├── .env
├── .gitignore
├── download_dataset.py
├── main.py
├── requirements.txt
└── README.md
```

## Banco de dados

- Banco: `netflix`
- Coleção: `netflix_titles`
- Formato: documentos JSON armazenados no MongoDB.

## Como executar

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Configure a variável `MONGODB_URI` no arquivo `.env`, utilizando sua string de conexão do MongoDB Atlas.

3. Execute o pipeline:

```bash
python main.py
```

## Resultado esperado

O pipeline realiza o processamento dos dados com Apache Spark, gera arquivos Parquet e carrega os documentos transformados na coleção `netflix_titles` do MongoDB Atlas.
