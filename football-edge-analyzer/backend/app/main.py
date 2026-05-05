from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.routers import ai, analysis, health, importers

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="MVP para análise de odds, valor esperado e normalização de dados de futebol.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(analysis.router)
app.include_router(importers.router)
app.include_router(ai.router)


@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "message": "Use /docs para testar os endpoints do MVP.",
        "risk_notice": "As análises não prometem lucro. Use gestão de risco e backtesting.",
    }
