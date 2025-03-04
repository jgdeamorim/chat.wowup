# Usa a imagem oficial do Python
FROM python:3.11

# Define o diretório de trabalho
WORKDIR /app

# Define a variável para garantir que o Python encontre os pacotes
ENV PYTHONPATH=/app

# Copia apenas os arquivos necessários primeiro
COPY requirements.txt .

# Instala as dependências antes de copiar o código
RUN pip install --no-cache-dir -r requirements.txt

# Copia apenas a pasta `app/` corretamente
COPY ./app /app

# Copia `main.py` e demais arquivos necessários
COPY main.py /app

# Exposição da porta
EXPOSE 8000

# Comando correto para rodar o FastAPI com Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
