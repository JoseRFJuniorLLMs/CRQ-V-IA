#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "   CRQ-V-IA: Plataforma de Prospecção Fiscal Inteligente   "
echo "   Conselho Regional de Química da 5ª Região (RS)         "
echo "=========================================================="

if [ ! -d "apps/api/.venv" ]; then
    echo "[1/3] Criando virtualenv e instalando pacotes..."
    uv venv apps/api/.venv --python 3.12
    uv pip install --python apps/api/.venv -r apps/api/requirements.txt
fi

if [ ! -f "crqvia.db" ]; then
    echo "[2/3] Executando seeds iniciais do RS..."
    apps/api/.venv/bin/python services/ingest/run_seed.py
fi

echo "[3/3] Iniciando servidor em http://0.0.0.0:8000..."
apps/api/.venv/bin/uvicorn apps.api.main:app --host 0.0.0.0 --port 8000
