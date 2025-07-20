from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/imobiliarias",
    tags=["Imobiliárias"]
)

@router.post("/", response_model=schemas.Imobiliaria)
def create_imobiliaria(imobiliaria: schemas.ImobiliariaCreate, db: Session = Depends(get_db)):
    if imobiliaria.imob_creci_juridico:
        db_imobiliaria = crud.get_imobiliaria_by_creci(db, creci=imobiliaria.imob_creci_juridico)
        if db_imobiliaria:
            raise HTTPException(status_code=400, detail="CRECI Jurídico já cadastrado")
    return crud.create_imobiliaria(db=db, imobiliaria=imobiliaria)

@router.get("/", response_model=List[schemas.Imobiliaria])
def read_imobiliarias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    imobiliarias = crud.get_imobiliarias(db, skip=skip, limit=limit)
    return imobiliarias

@router.get("/{imobiliaria_id}", response_model=schemas.Imobiliaria)
def read_imobiliaria(imobiliaria_id: int, db: Session = Depends(get_db)):
    db_imobiliaria = crud.get_imobiliaria(db, imobiliaria_id=imobiliaria_id)
    if db_imobiliaria is None:
        raise HTTPException(status_code=404, detail="Imobiliária não encontrada")
    return db_imobiliaria
