# backend/app/schemas.py
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional, List
from datetime import datetime
from .models import ImobiliariaStatus, UsuarioPermissao, EmpreendimentoStatus, ArquivoTipo

# --- Schemas de Token ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Schemas de Imobiliaria ---
class ImobiliariaBase(BaseModel):
    imob_nome: str
    imob_creci_juridico: Optional[str] = None
    imob_logo_url: Optional[str] = None
    status: ImobiliariaStatus = ImobiliariaStatus.pendente

class ImobiliariaCreate(ImobiliariaBase):
    pass

class ImobiliariaUpdate(BaseModel):
    imob_nome: Optional[str] = None
    imob_creci_juridico: Optional[str] = None
    imob_logo_url: Optional[str] = None
    status: Optional[ImobiliariaStatus] = None

class Imobiliaria(ImobiliariaBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Schemas de Usuario ---
class UsuarioBase(BaseModel):
    usu_nome: str
    usu_email: EmailStr
    usu_creci: Optional[str] = None
    permissao: UsuarioPermissao = UsuarioPermissao.usuario

class UsuarioCreate(UsuarioBase):
    imobiliaria_id: int
    usu_senha: str

class Usuario(UsuarioBase):
    id: int
    imobiliaria_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Schemas de Arquivo ---
class ArquivoBase(BaseModel):
    tipo: ArquivoTipo
    link_arquivo: str

class ArquivoCreate(ArquivoBase):
    pass

class Arquivo(ArquivoBase):
    id: int
    empreendimento_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Schemas de Empreendimento ---
class EmpreendimentoBase(BaseModel):
    emp_nome: str
    emp_status: EmpreendimentoStatus
    emp_endereco: Optional[str] = None
    emp_descricao: Optional[str] = None
    emp_itens_de_lazer: Optional[List[str]] = None
    emp_metragens: Optional[str] = None
    valor_inicial: Optional[float] = None

class EmpreendimentoCreate(EmpreendimentoBase):
    pass

class Empreendimento(EmpreendimentoBase):
    id: int
    imobiliaria_id: int
    created_at: datetime
    updated_at: datetime
    arquivos: List[Arquivo] = []
    model_config = ConfigDict(from_attributes=True)

# Schema para exibir imobiliária com seus usuários e empreendimentos
class ImobiliariaCompleta(Imobiliaria):
    usuarios: List[Usuario] = []
    empreendimentos: List[Empreendimento] = []
