# backend/app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas, security

# --- CRUD para Imobiliaria (sem alterações) ---
def get_imobiliaria(db: Session, imobiliaria_id: int):
    return db.query(models.Imobiliaria).filter(models.Imobiliaria.id == imobiliaria_id).first()

def get_imobiliarias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Imobiliaria).offset(skip).limit(limit).all()

def create_imobiliaria(db: Session, imobiliaria: schemas.ImobiliariaCreate):
    db_imobiliaria = models.Imobiliaria(**imobiliaria.model_dump())
    db.add(db_imobiliaria)
    db.commit()
    db.refresh(db_imobiliaria)
    return db_imobiliaria

def update_imobiliaria(db: Session, imobiliaria_id: int, imobiliaria_update: schemas.ImobiliariaUpdate):
    db_imobiliaria = get_imobiliaria(db, imobiliaria_id)
    if not db_imobiliaria:
        return None
    update_data = imobiliaria_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_imobiliaria, key, value)
    db.commit()
    db.refresh(db_imobiliaria)
    return db_imobiliaria

def delete_imobiliaria(db: Session, imobiliaria_id: int):
    db_imobiliaria = get_imobiliaria(db, imobiliaria_id)
    if not db_imobiliaria:
        return None
    db.delete(db_imobiliaria)
    db.commit()
    return db_imobiliaria

# --- CRUD para Usuario (Atualizado) ---
def get_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

def get_usuario_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.usu_email == email).first()

def get_usuarios_by_imobiliaria(db: Session, imobiliaria_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario).filter(models.Usuario.imobiliaria_id == imobiliaria_id).offset(skip).limit(limit).all()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    hashed_password = security.get_password_hash(usuario.usu_senha)
    db_usuario = models.Usuario(
        usu_nome=usuario.usu_nome,
        usu_email=usuario.usu_email,
        usu_senha=hashed_password,
        usu_apelido=usuario.usu_apelido, # NOVO CAMPO
        usu_creci=usuario.usu_creci,
        permissao=usuario.permissao,
        imobiliaria_id=usuario.imobiliaria_id
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# --- CRUD para Empreendimento (Atualizado) ---
def get_empreendimento(db: Session, empreendimento_id: int):
    return db.query(models.Empreendimento).filter(models.Empreendimento.id == empreendimento_id).first()

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

# --- CRUD para Arquivo (Atualizado) ---
def create_arquivo(db: Session, arquivo: schemas.ArquivoCreate):
    db_arquivo = models.Arquivo(**arquivo.model_dump())
    db.add(db_arquivo)
    db.commit()
    db.refresh(db_arquivo)
    return db_arquivo

def delete_arquivo(db: Session, arquivo_id: int):
    db_arquivo = db.query(models.Arquivo).filter(models.Arquivo.id == arquivo_id).first()
    if not db_arquivo:
        return None
    db.delete(db_arquivo)
    db.commit()
    return db_arquivo
