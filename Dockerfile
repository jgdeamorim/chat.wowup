# Usa a imagem oficial do Python
FROM python:3.11

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de dependências primeiro para otimizar o cache do Docker
COPY requirements.txt .

# Instala as dependências sem cache para evitar problemas
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código para o container
COPY . /app

# Expõe a porta do FastAPI
EXPOSE 8000

# Executa o FastAPI com Uvicorn na porta correta
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
