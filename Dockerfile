# Usa uma imagem leve do Python
FROM python:3.9-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia os arquivos necessários
COPY requirements.txt requirements.txt

# Instala as dependências
RUN pip install -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta 5000
EXPOSE 5000

# Comando para rodar a app
CMD ["python", "app.py"]