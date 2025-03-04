# Usa a imagem oficial do Python
FROM python:3.11

# Define o diretório de trabalho
WORKDIR /app

# Define a variável para encontrar pacotes Python corretamente
ENV PYTHONPATH=/app

# Copia os arquivos de dependências primeiro para melhorar cache
COPY requirements.txt .

# Instala as dependências antes de copiar o código
RUN pip install --no-cache-dir -r requirements.txt

# Copia a pasta `app/` corretamente e o `main.py`
COPY . .

# Expõe a porta
EXPOSE 8000

# Comando correto para rodar FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
