# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import imobiliarias, auth, usuarios, empreendimentos, arquivos

# Cria todas as tabelas na base de dados se não existirem
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Catálogo de Empreendimentos API",
    description="API completa para o sistema de catálogo de empreendimentos imobiliários.",
    version="1.1.0"
)

# --- CONFIGURAÇÃO DE CORS PERMISSIVA ---
# O asterisco (*) permite que qualquer origem (qualquer site)
# faça requisições para a sua API, resolvendo o problema.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todos os cabeçalhos
)
# --- FIM DA CONFIGURAÇÃO DE CORS ---


# Inclui todos os routers com um prefixo global /api
app.include_router(auth.router, prefix="/api")
app.include_router(imobiliarias.router, prefix="/api")
app.include_router(usuarios.router, prefix="/api")
app.include_router(empreendimentos.router, prefix="/api")
app.include_router(arquivos.router, prefix="/api")

@app.get("/")
def read_root():
    return {"Status": "API Online"}
