# backend/app/schemas.py
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional, List
from datetime import datetime, date
# MUDANÇA: Importando do novo arquivo enums.py
from .enums import ImobiliariaStatus, UsuarioPermissao, EmpreendimentoStatus, ArquivoTipo

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
    usu_apelido: Optional[str] = None
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
    ordem: Optional[int] = 0

class ArquivoCreate(ArquivoBase):
    empreendimento_id: int

class Arquivo(ArquivoBase):
    id: int
    empreendimento_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Schemas de Empreendimento ---
class EmpreendimentoBase(BaseModel):
    emp_nome: str
    emp_apelido: Optional[str] = None
    emp_status: EmpreendimentoStatus
    emp_endereco: Optional[str] = None
    regiao: Optional[str] = None
    emp_descricao: Optional[str] = None
    emp_itens_de_lazer: Optional[List[str]] = None
    emp_locais_proximos: Optional[List[str]] = None
    emp_metragens: Optional[str] = None
    emp_suites: Optional[str] = None
    emp_banheiros: Optional[str] = None
    emp_vagas: Optional[str] = None
    emp_diferenciais: Optional[List[str]] = None
    emp_arquitetura: Optional[str] = None
    emp_construtora: Optional[str] = None
    emp_incorporadora: Optional[str] = None
    numero_torres: Optional[int] = None
    numero_apartamentos: Optional[int] = None
    area_terreno: Optional[float] = None
    area_construcao: Optional[float] = None
    valor_inicial: Optional[float] = None
    valor_final: Optional[float] = None
    emp_previsao: Optional[date] = None
    emp_link_publico: Optional[str] = None

class EmpreendimentoCreate(EmpreendimentoBase):
    pass

class EmpreendimentoUpdate(EmpreendimentoBase):
    emp_nome: Optional[str] = None
    emp_status: Optional[EmpreendimentoStatus] = None

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
