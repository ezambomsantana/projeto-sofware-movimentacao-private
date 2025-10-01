FROM python:3.11-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia dependências primeiro (melhora cache das camadas)
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código
COPY . .

# Expõe a porta do Flask
EXPOSE 5000

# Variável para o Flask rodar "production ready"
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Comando de execução
CMD ["flask", "run"]