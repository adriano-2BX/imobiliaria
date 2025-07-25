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
    # VERIFICAÇÃO ADICIONADA: Checa se o link público já existe antes de tentar criar.
    if empreendimento.emp_link_publico:
        db_empreendimento = crud.get_empreendimento_by_link(db, link=empreendimento.emp_link_publico)
        if db_empreendimento:
            raise HTTPException(status_code=400, detail="O Link Público informado já está em uso.")
            
    return crud.create_empreendimento(db=db, empreendimento=empreendimento, imobiliaria_id=current_user.imobiliaria_id)

@router.get("/", response_model=List[schemas.Empreendimento])
def read_empreendimentos(db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(security.get_current_user), skip: int = 0, limit: int = 100):
    return crud.get_empreendimentos_by_imobiliaria(db, imobiliaria_id=current_user.imobiliaria_id, skip=skip, limit=limit)

@router.get("/{empreendimento_id}", response_model=schemas.Empreendimento)
def read_empreendimento(empreendimento_id: int, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(security.get_current_user)):
    db_empreendimento = crud.get_empreendimento(db, empreendimento_id)
    if db_empreendimento is None:
        raise HTTPException(status_code=404, detail="Empreendimento não encontrado")
    if db_empreendimento.imobiliaria_id != current_user.imobiliaria_id:
        raise HTTPException(status_code=403, detail="Acesso não autorizado a este empreendimento")
    return db_empreendimento

@router.put("/{empreendimento_id}", response_model=schemas.Empreendimento)
def update_empreendimento(empreendimento_id: int, empreendimento_update: schemas.EmpreendimentoUpdate, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(security.get_current_user)):
    db_empreendimento = crud.get_empreendimento(db, empreendimento_id)
    if db_empreendimento is None:
        raise HTTPException(status_code=404, detail="Empreendimento não encontrado")
    if db_empreendimento.imobiliaria_id != current_user.imobiliaria_id:
        raise HTTPException(status_code=403, detail="Acesso não autorizado a este empreendimento")
    
    # Adiciona uma verificação de duplicidade também no update
    if empreendimento_update.emp_link_publico and empreendimento_update.emp_link_publico != db_empreendimento.emp_link_publico:
        link_exists = crud.get_empreendimento_by_link(db, link=empreendimento_update.emp_link_publico)
        if link_exists:
            raise HTTPException(status_code=400, detail="O Link Público informado já está em uso por outro empreendimento.")

    updated_empreendimento = crud.update_empreendimento(db, empreendimento_id, empreendimento_update)
    return updated_empreendimento

@router.delete("/{empreendimento_id}", response_model=schemas.Empreendimento)
def delete_empreendimento(empreendimento_id: int, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(security.get_current_user)):
    db_empreendimento = crud.get_empreendimento(db, empreendimento_id)
    if db_empreendimento is None:
        raise HTTPException(status_code=404, detail="Empreendimento não encontrado")
    if db_empreendimento.imobiliaria_id != current_user.imobiliaria_id:
        raise HTTPException(status_code=403, detail="Acesso não autorizado a este empreendimento")
        
    deleted_empreendimento = crud.delete_empreendimento(db, empreendimento_id)
    return deleted_empreendimento
