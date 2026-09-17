# Script de Inicialização Rápida da Plataforma CRQ-V-IA
$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   CRQ-V-IA: Plataforma de Prospecção Fiscal Inteligente   " -ForegroundColor Green
Write-Host "   Conselho Regional de Química da 5ª Região (RS)         " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$VENV_PYTHON = "apps\api\.venv\Scripts\python.exe"

# 1. Verifica ou cria virtualenv
if (-not (Test-Path $VENV_PYTHON)) {
    Write-Host "`n[1/3] Criando ambiente virtual com uv..." -ForegroundColor Yellow
    uv venv apps\api\.venv --python 3.12
    Write-Host "[1/3] Instalando dependências..." -ForegroundColor Yellow
    uv pip install --python apps\api\.venv -r apps\api\requirements.txt
} else {
    Write-Host "`n[1/3] Ambiente virtual localizado." -ForegroundColor Green
}

# 2. Verifica se a base de dados já foi semeada
if (-not (Test-Path "crqvia.db")) {
    Write-Host "[2/3] Inicializando banco e executando seeds do RS..." -ForegroundColor Yellow
    & $VENV_PYTHON services\ingest\run_seed.py
} else {
    Write-Host "[2/3] Base de dados crqvia.db já inicializada." -ForegroundColor Green
}

# 3. Abre o navegador e inicia o servidor
Write-Host "[3/3] Iniciando servidor em http://localhost:8000..." -ForegroundColor Green
Write-Host "`nPressione Ctrl+C para encerrar o servidor.`n" -ForegroundColor DarkGray

Start-Process "http://localhost:8000"

& $VENV_PYTHON -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8000
