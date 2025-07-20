# 1. Usar uma imagem oficial do Python como base
FROM python:3.11-slim

# 2. Definir o diretório de trabalho para /code
WORKDIR /code

# 3. Copiar o arquivo de dependências para o novo diretório
COPY requirements.txt .

# 4. Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar todo o nosso código para o diretório /code
# Agora a estrutura dentro do container será /code/app/...
COPY . .

# 6. Expor a porta que a nossa aplicação vai usar
EXPOSE 8000

# 7. Definir o comando para iniciar a API (continua o mesmo)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
