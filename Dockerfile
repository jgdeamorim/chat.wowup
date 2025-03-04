# Usa a imagem oficial do Python
FROM python:3.11

# Define o diretório de trabalho
WORKDIR /app

ENV PYTHONPATH=/app

# Copia os arquivos necessários para dentro do container
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do backend
COPY . .

# Exposição da porta
EXPOSE 8000

# Comando correto para rodar o FastAPI com Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
