# 1. Usar uma imagem oficial do Python como base
FROM python:3.11-slim

# 2. Definir o diretório de trabalho dentro do container
WORKDIR /app

# 3. Instalar dependências do sistema, se necessário (bom para mysqlclient)
# RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc && rm -rf /var/lib/apt/lists/*

# 4. Copiar o arquivo de dependências para o container
COPY requirements.txt .

# 5. Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar todo o código da nossa pasta "app" para o container
COPY ./app /app

# 7. Expor a porta que a nossa aplicação vai usar dentro do container
EXPOSE 8000

# 8. Definir o comando para iniciar a API quando o container rodar
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
