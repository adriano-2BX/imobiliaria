# backend/app/routers/empreendimentos.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas, security, database

router = APIRouter(
    prefix="/empreendimentos",
    tags=["Empreendimentos"]
)

@router.post("/", response_model=schemas.Empreendimento, status_code=201)
def create_empreendimento(empreendimento: schemas.EmpreendimentoCreate, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(security.get_current_user)):
    # Cria um empreendimento para a imobiliária do usuário logado
    return crud.create_empreendimento(db=db, empreendimento=empreendimento, imobiliaria_id=current_user.imobiliaria_id)

@router.get("/", response_model=List[schemas.Empreendimento])
def read_empreendimentos(db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(security.get_current_user), skip: int = 0, limit: int = 100):
    # Lista apenas os empreendimentos da imobiliária do usuário logado
    return crud.get_empreendimentos_by_imobiliaria(db, imobiliaria_id=current_user.imobiliaria_id, skip=skip, limit=limit)

@router.get("/{empreendimento_id}", response_model=schemas.Empreendimento)
def read_empreendimento(empreendimento_id: int, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(security.get_current_user)):
    db_empreendimento = crud.get_empreendimento(db, empreendimento_id)
    if db_empreendimento is None:
        raise HTTPException(status_code=404, detail="Empreendimento não encontrado")
    # Garante que o usuário só possa ver empreendimentos da sua própria imobiliária
    if db_empreendimento.imobiliaria_id != current_user.imobiliaria_id:
        raise HTTPException(status_code=403, detail="Acesso não autorizado a este empreendimento")
    return db_empreendimento

# Adicionar rotas para UPDATE e DELETE aqui, seguindo o mesmo padrão de segurança
