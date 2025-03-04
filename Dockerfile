# Usa a imagem oficial do Python
FROM python:3.11

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências primeiro para melhorar cache
COPY requirements.txt .

# Instala as dependências antes de copiar o código
RUN pip install --no-cache-dir -r requirements.txt

# Copia apenas o conteúdo da pasta `app/`, não a pasta inteira
COPY app/ /app/

# Ajusta a variável de ambiente para garantir que os módulos sejam encontrados corretamente
ENV PYTHONPATH=/app

# Expõe a porta
EXPOSE 8000

# Comando correto para rodar FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
