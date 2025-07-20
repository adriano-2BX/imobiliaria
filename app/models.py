# backend/app/models.py
from sqlalchemy import (Column, Integer, String, Enum, TIMESTAMP, text, ForeignKey,
                        DECIMAL, Date, JSON, Text)
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

# ENUM ATUALIZADO
class EmpreendimentoStatus(str, enum.Enum):
    lancamento = "lancamento"
    em_obras = "em_obras"
    pronto_para_morar = "pronto_para_morar"
    entregue = "entregue"

# ENUM ATUALIZADO
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
    usu_apelido = Column(String(100), nullable=True)
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
    emp_apelido = Column(String(255), nullable=True)
    emp_status = Column(Enum(EmpreendimentoStatus), nullable=False) # Usa o Enum atualizado
    emp_endereco = Column(Text, nullable=True)
    regiao = Column(String(255), nullable=True)
    emp_descricao = Column(Text, nullable=True)
    emp_itens_de_lazer = Column(JSON, nullable=True)
    emp_locais_proximos = Column(JSON, nullable=True)
    emp_metragens = Column(String(255), nullable=True)
    emp_suites = Column(String(100), nullable=True)
    emp_banheiros = Column(String(100), nullable=True)
    emp_vagas = Column(String(100), nullable=True)
    emp_diferenciais = Column(JSON, nullable=True)
    emp_arquitetura = Column(String(255), nullable=True)
    emp_construtora = Column(String(255), nullable=True)
    emp_incorporadora = Column(String(255), nullable=True)
    numero_torres = Column(Integer, nullable=True)
    numero_apartamentos = Column(Integer, nullable=True)
    area_terreno = Column(DECIMAL(10, 2), nullable=True)
    area_construcao = Column(DECIMAL(10, 2), nullable=True)
    valor_inicial = Column(DECIMAL(12, 2), nullable=True)
    valor_final = Column(DECIMAL(12, 2), nullable=True)
    emp_previsao = Column(Date, nullable=True)
    emp_link_publico = Column(String(255), nullable=True, unique=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    imobiliaria = relationship("Imobiliaria", back_populates="empreendimentos")
    arquivos = relationship("Arquivo", back_populates="empreendimento", cascade="all, delete-orphan")

class Arquivo(Base):
    __tablename__ = "arquivos"
    id = Column(Integer, primary_key=True, index=True)
    empreendimento_id = Column(Integer, ForeignKey("empreendimentos.id"), nullable=False)
    tipo = Column(Enum(ArquivoTipo), nullable=False) # Usa o Enum atualizado
    link_arquivo = Column(String(255), nullable=False)
    ordem = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    empreendimento = relationship("Empreendimento", back_populates="arquivos")
