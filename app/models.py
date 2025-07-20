# backend/app/models.py
from sqlalchemy import (Column, Integer, String, Enum, TIMESTAMP, text, ForeignKey,
                        DECIMAL, Date, JSON)
from sqlalchemy.orm import relationship
from .database import Base
import enum

# --- Enums para status e tipos ---
class ImobiliariaStatus(str, enum.Enum):
    ativo = "ativo"
    inativo = "inativo"
    pendente = "pendente"

class UsuarioPermissao(str, enum.Enum):
    admin = "admin"
    usuario = "usuario"

class EmpreendimentoStatus(str, enum.Enum):
    lancamento = "lançamento"
    em_obras = "em obras"
    pronto_para_morar = "pronto para morar"
    entregue = "entregue"

class ArquivoTipo(str, enum.Enum):
    imagem_fachada = "imagem_fachada"
    imagem_interna = "imagem_interna"
    planta = "planta"
    video = "video"
    tour_360 = "tour_360"

# --- Modelos das Tabelas ---

class Imobiliaria(Base):
    __tablename__ = "imobiliarias"
    id = Column(Integer, primary_key=True, index=True)
    imob_nome = Column(String(255), nullable=False)
    imob_creci_juridico = Column(String(50), unique=True, index=True)
    imob_logo_url = Column(String(255), nullable=True)
    status = Column(Enum(ImobiliariaStatus), default=ImobiliariaStatus.pendente)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    usuarios = relationship("Usuario", back_populates="imobiliaria")
    empreendimentos = relationship("Empreendimento", back_populates="imobiliaria")

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    imobiliaria_id = Column(Integer, ForeignKey("imobiliarias.id"), nullable=False)
    usu_nome = Column(String(255), nullable=False)
    usu_email = Column(String(255), nullable=False, unique=True, index=True)
    usu_senha = Column(String(255), nullable=False)
    usu_creci = Column(String(50), unique=True, nullable=True)
    permissao = Column(Enum(UsuarioPermissao), default=UsuarioPermissao.usuario)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    imobiliaria = relationship("Imobiliaria", back_populates="usuarios")

class Empreendimento(Base):
    __tablename__ = "empreendimentos"
    id = Column(Integer, primary_key=True, index=True)
    imobiliaria_id = Column(Integer, ForeignKey("imobiliarias.id"), nullable=False)
    emp_nome = Column(String(255), nullable=False)
    emp_status = Column(Enum(EmpreendimentoStatus), nullable=False)
    emp_endereco = Column(String(500))
    emp_descricao = Column(String(2000))
    emp_itens_de_lazer = Column(JSON)
    emp_metragens = Column(String(255))
    valor_inicial = Column(DECIMAL(12, 2))
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    imobiliaria = relationship("Imobiliaria", back_populates="empreendimentos")
    arquivos = relationship("Arquivo", back_populates="empreendimento", cascade="all, delete-orphan")

class Arquivo(Base):
    __tablename__ = "arquivos"
    id = Column(Integer, primary_key=True, index=True)
    empreendimento_id = Column(Integer, ForeignKey("empreendimentos.id"), nullable=False)
    tipo = Column(Enum(ArquivoTipo), nullable=False)
    link_arquivo = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    empreendimento = relationship("Empreendimento", back_populates="arquivos")
