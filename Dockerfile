# Usa a imagem oficial do Python
FROM python:3.11

# Define o diretório de trabalho
WORKDIR /app

# Define a variável PYTHONPATH
ENV PYTHONPATH=/app

# Copia apenas as dependências primeiro para aproveitar o cache
COPY requirements.txt .

# Instala as dependências antes de copiar o código-fonte
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do backend
COPY . .

# Exposição da porta
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
