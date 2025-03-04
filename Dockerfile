# Usa a imagem oficial do Python
FROM python:3.11

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos de dependências primeiro para melhor cache
COPY requirements.txt .

# Instala as dependências antes de copiar o código
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do projeto
COPY . .

# Define o PYTHONPATH para o projeto reconhecer os módulos corretamente
ENV PYTHONPATH=/app

# Expõe a porta para o serviço
EXPOSE 8000

# Comando correto para rodar FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
