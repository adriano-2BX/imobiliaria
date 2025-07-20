# backend/app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas, security

# --- CRUD para Imobiliaria (sem alterações) ---
# ... (código existente) ...

# --- CRUD para Usuario (sem alterações) ---
# ... (código existente) ...

# --- CRUD para Empreendimento (Atualizado) ---
def get_empreendimento(db: Session, empreendimento_id: int):
    return db.query(models.Empreendimento).filter(models.Empreendimento.id == empreendimento_id).first()

# NOVA FUNÇÃO
def get_empreendimento_by_link(db: Session, link: str):
    return db.query(models.Empreendimento).filter(models.Empreendimento.emp_link_publico == link).first()

def get_empreendimentos_by_imobiliaria(db: Session, imobiliaria_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Empreendimento).filter(models.Empreendimento.imobiliaria_id == imobiliaria_id).offset(skip).limit(limit).all()

def create_empreendimento(db: Session, empreendimento: schemas.EmpreendimentoCreate, imobiliaria_id: int):
    db_empreendimento = models.Empreendimento(**empreendimento.model_dump(), imobiliaria_id=imobiliaria_id)
    db.add(db_empreendimento)
    db.commit()
    db.refresh(db_empreendimento)
    return db_empreendimento

def update_empreendimento(db: Session, empreendimento_id: int, empreendimento_update: schemas.EmpreendimentoUpdate):
    db_empreendimento = get_empreendimento(db, empreendimento_id)
    if not db_empreendimento:
        return None
    update_data = empreendimento_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_empreendimento, key, value)
    db.commit()
    db.refresh(db_empreendimento)
    return db_empreendimento

def delete_empreendimento(db: Session, empreendimento_id: int):
    db_empreendimento = get_empreendimento(db, empreendimento_id)
    if not db_empreendimento:
        return None
    db.delete(db_empreendimento)
    db.commit()
    return db_empreendimento

# --- CRUD para Arquivo (sem alterações) ---
# ... (código existente) ...
