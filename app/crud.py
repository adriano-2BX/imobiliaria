from sqlalchemy.orm import Session
from . import models, schemas

def get_imobiliaria(db: Session, imobiliaria_id: int):
    return db.query(models.Imobiliaria).filter(models.Imobiliaria.id == imobiliaria_id).first()

def get_imobiliaria_by_creci(db: Session, creci: str):
    return db.query(models.Imobiliaria).filter(models.Imobiliaria.imob_creci_juridico == creci).first()

def get_imobiliarias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Imobiliaria).offset(skip).limit(limit).all()

def create_imobiliaria(db: Session, imobiliaria: schemas.ImobiliariaCreate):
    db_imobiliaria = models.Imobiliaria(
        imob_nome=imobiliaria.imob_nome,
        imob_creci_juridico=imobiliaria.imob_creci_juridico,
        status=imobiliaria.status
    )
    db.add(db_imobiliaria)
    db.commit()
    db.refresh(db_imobiliaria)
    return db_imobiliaria
