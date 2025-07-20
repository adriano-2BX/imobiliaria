from fastapi import FastAPI
from .database import engine
from . import models
from .routers import imobiliarias

# Esta linha cria a tabela no banco de dados se ela não existir
# Ao conectar com um banco de dados externo, certifique-se de que o usuário tem permissão para CREATE TABLE
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Catálogo de Empreendimentos API",
    description="API para o sistema de catálogo de empreendimentos imobiliários.",
    version="0.1.0"
)

# Inclui os routers
app.include_router(imobiliarias.router)

@app.get("/")
def read_root():
    return {"Status": "API Online"}
