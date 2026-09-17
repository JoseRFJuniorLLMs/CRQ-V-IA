from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path

from apps.api.core.config import settings
from apps.api.core.database import init_db
from apps.api.routers import auth, prospects, lists, exports, stats, audit, health

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa tabelas
    init_db()
    yield

app = FastAPI(
    title=settings.APP_NAME,
    description="Plataforma de Prospecção Fiscal Especializada em Química - CRQ-V (Rio Grande do Sul)",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra Routers
app.include_router(health.router, prefix=settings.API_PREFIX)
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(prospects.router, prefix=settings.API_PREFIX)
app.include_router(lists.router, prefix=settings.API_PREFIX)
app.include_router(exports.router, prefix=settings.API_PREFIX)
app.include_router(stats.router, prefix=settings.API_PREFIX)
app.include_router(audit.router, prefix=settings.API_PREFIX)

# Monta frontend estático se compilado
web_dist = Path(__file__).resolve().parent.parent / "web" / "dist"
if web_dist.exists() and (web_dist / "index.html").exists():
    app.mount("/", StaticFiles(directory=str(web_dist), html=True), name="frontend")
else:
    @app.get("/")
    def root_welcome():
        return {
            "message": "CRQ-V-IA API Online",
            "docs": "/docs",
            "status": "Operacional",
            "target": "Conselho Regional de Química da 5ª Região (RS)"
        }
