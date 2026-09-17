FROM python:3.12-slim

WORKDIR /app

# Dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala uv para builds ultra-rápidos
RUN pip install --no-cache-dir uv

# Copia arquivos de requisitos e instala
COPY apps/api/requirements.txt /app/apps/api/requirements.txt
RUN uv pip install --system -r /app/apps/api/requirements.txt

# Copia código da aplicação e frontend compilado
COPY apps /app/apps
COPY services /app/services

# Variáveis de ambiente padrão
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV DATABASE_URL=sqlite:///./crqvia.db

# Executa seed inicial e inicia o servidor
EXPOSE 8000
CMD ["sh", "-c", "python services/ingest/run_seed.py && uvicorn apps.api.main:app --host 0.0.0.0 --port 8000"]
