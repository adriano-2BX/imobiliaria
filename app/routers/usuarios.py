# backend/app/routers/usuarios.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas, security, database

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)

@router.post("/", response_model=schemas.Usuario, status_code=201)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(database.get_db)):
    # Em um sistema real, esta rota seria protegida por um admin da imobiliária
    db_user = crud.get_usuario_by_email(db, email=usuario.usu_email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    return crud.create_usuario(db=db, usuario=usuario)

@router.get("/me", response_model=schemas.Usuario)
def read_users_me(current_user: models.Usuario = Depends(security.get_current_user)):
    # Rota para o usuário logado ver seus próprios dados
    return current_user
