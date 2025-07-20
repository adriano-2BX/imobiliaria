# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import imobiliarias, auth, usuarios, empreendimentos

# Cria todas as tabelas no banco de dados se não existirem
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Catálogo de Empreendimentos API",
    description="API completa para o sistema de catálogo de empreendimentos imobiliários.",
    version="1.0.0"
)

# --- INÍCIO DA CONFIGURAÇÃO DO CORS ---
#
# Para permitir qualquer integração, definimos a lista de origens como ["*"]
# O asterisco (*) é um curinga que significa "permitir qualquer origem".
#
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], # Permite todos os cabeçalhos
)
# --- FIM DA CONFIGURAÇÃO DO CORS ---


# Inclui todos os routers com um prefixo global /api
app.include_router(auth.router, prefix="/api")
app.include_router(imobiliarias.router, prefix="/api")
app.include_router(usuarios.router, prefix="/api")
app.include_router(empreendimentos.router, prefix="/api")

@app.get("/")
def read_root():
    return {"Status": "API Online"}
