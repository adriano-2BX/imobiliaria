# backend/app/routers/arquivos.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas, security, database

router = APIRouter(
    prefix="/arquivos",
    tags=["Arquivos"]
)

@router.post("/", response_model=schemas.Arquivo, status_code=201)
def create_arquivo(arquivo: schemas.ArquivoCreate, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(security.get_current_user)):
    # Verifica se o empreendimento ao qual o arquivo pertence é da imobiliária do usuário
    db_empreendimento = crud.get_empreendimento(db, arquivo.empreendimento_id)
    if not db_empreendimento:
        raise HTTPException(status_code=404, detail="Empreendimento não encontrado")
    if db_empreendimento.imobiliaria_id != current_user.imobiliaria_id:
        raise HTTPException(status_code=403, detail="Não autorizado a adicionar arquivos a este empreendimento")
        
    return crud.create_arquivo(db=db, arquivo=arquivo)

@router.delete("/{arquivo_id}", response_model=schemas.Arquivo)
def delete_arquivo(arquivo_id: int, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(security.get_current_user)):
    db_arquivo = db.query(models.Arquivo).filter(models.Arquivo.id == arquivo_id).first()
    if not db_arquivo:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    
    # Verifica a permissão através do empreendimento pai
    db_empreendimento = crud.get_empreendimento(db, db_arquivo.empreendimento_id)
    if db_empreendimento.imobiliaria_id != current_user.imobiliaria_id:
        raise HTTPException(status_code=403, detail="Não autorizado a deletar este arquivo")
        
    deleted_arquivo = crud.delete_arquivo(db, arquivo_id=arquivo_id)
    return deleted_arquivo
