# Usa imagem oficial do Python
FROM python:3.11-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do seu projeto para o container
COPY . /app

# Instala dependências
RUN pip install --upgrade pip
RUN pip install fastapi uvicorn

# Expõe a porta usada pelo Uvicorn
EXPOSE 8000

# Comando para iniciar o servidor FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

