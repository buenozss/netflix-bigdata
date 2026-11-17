
import kagglehub
import shutil
import os

# Baixar a base de dados da Netflix
path = kagglehub.dataset_download("shivamb/netflix-shows")

print("Dataset baixado em:", path)

# Criar a pasta de destino
os.makedirs("data/raw", exist_ok=True)

# Copiar o CSV para dentro do projeto
arquivo_origem = os.path.join(path, "netflix_titles.csv")
arquivo_destino = "data/raw/netflix_titles.csv"

shutil.copy2(arquivo_origem, arquivo_destino)

print("Arquivo CSV salvo em:", arquivo_destino)
