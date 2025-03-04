# Usa a imagem oficial do Python
FROM python:3.11

# Define o diretório de trabalho como raiz "/"
WORKDIR /

# Copia os arquivos de dependências primeiro
COPY requirements.txt .

# Instala as dependências antes de copiar o código
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos diretamente para a raiz do container
COPY . /

# Expõe a porta do FastAPI
EXPOSE 8000

# Comando correto para rodar FastAPI sem precisar de ajustes no caminho
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
