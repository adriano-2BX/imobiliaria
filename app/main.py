# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import imobiliarias, auth, usuarios, empreendimentos, arquivos # ADICIONADO

# Cria todas as tabelas no banco de dados se não existirem
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Catálogo de Empreendimentos API",
    description="API completa para o sistema de catálogo de empreendimentos imobiliários.",
    version="1.1.0" # Versão atualizada
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui todos os routers com um prefixo global /api
app.include_router(auth.router, prefix="/api")
app.include_router(imobiliarias.router, prefix="/api")
app.include_router(usuarios.router, prefix="/api")
app.include_router(empreendimentos.router, prefix="/api")
app.include_router(arquivos.router, prefix="/api") # NOVO ROUTER

@app.get("/")
def read_root():
    return {"Status": "API Online"}
