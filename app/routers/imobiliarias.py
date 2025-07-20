# backend/app/routers/imobiliarias.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas, security, database

router = APIRouter(
    prefix="/imobiliarias",
    tags=["Imobiliárias"]
)

@router.post("/", response_model=schemas.Imobiliaria, status_code=201)
def create_imobiliaria(imobiliaria: schemas.ImobiliariaCreate, db: Session = Depends(database.get_db)):
    # Em um sistema real, esta rota seria protegida por um SuperAdmin
    return crud.create_imobiliaria(db=db, imobiliaria=imobiliaria)

@router.get("/", response_model=List[schemas.Imobiliaria])
def read_imobiliarias(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_imobiliarias(db, skip=skip, limit=limit)

@router.get("/{imobiliaria_id}", response_model=schemas.ImobiliariaCompleta)
def read_imobiliaria(imobiliaria_id: int, db: Session = Depends(database.get_db)):
    db_imobiliaria = crud.get_imobiliaria(db, imobiliaria_id=imobiliaria_id)
    if db_imobiliaria is None:
        raise HTTPException(status_code=404, detail="Imobiliária não encontrada")
    return db_imobiliaria

@router.put("/{imobiliaria_id}", response_model=schemas.Imobiliaria)
def update_imobiliaria(imobiliaria_id: int, imobiliaria_update: schemas.ImobiliariaUpdate, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(security.get_current_admin_user)):
    # Protegido: Apenas admins podem atualizar.
    # Lógica adicional pode ser necessária para garantir que o admin pertence à imobiliária correta.
    db_imobiliaria = crud.update_imobiliaria(db, imobiliaria_id, imobiliaria_update)
    if db_imobiliaria is None:
        raise HTTPException(status_code=404, detail="Imobiliária não encontrada")
    return db_imobiliaria

@router.delete("/{imobiliaria_id}", response_model=schemas.Imobiliaria)
def delete_imobiliaria(imobiliaria_id: int, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(security.get_current_admin_user)):
    # Protegido: Apenas admins podem deletar.
    db_imobiliaria = crud.delete_imobiliaria(db, imobiliaria_id)
    if db_imobiliaria is None:
        raise HTTPException(status_code=404, detail="Imobiliária não encontrada")
    return db_imobiliaria
