# 🔹 Usando Python 3.11 (ou outra versão necessária)
FROM python:3.11

# 🔹 Definir diretório de trabalho dentro do container
WORKDIR /

# 🔹 Copiar arquivos do projeto para dentro do container
COPY . /app

# 🔹 Instalar dependências
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# 🔹 Expor porta do serviço
EXPOSE 8000

# 🔹 Comando para rodar o FastAPI com Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
