# backend/app/models.py
from sqlalchemy import (Column, Integer, String, TIMESTAMP, text, ForeignKey,
                        DECIMAL, Date, JSON, Text)
from sqlalchemy.orm import relationship
from .database import Base
# O import do 'enum' não é mais necessário aqui para os modelos de tabela

# Os Enums do Python ainda são usados nos Schemas para validação de entrada, então os mantemos.
from .schemas import ImobiliariaStatus, UsuarioPermissao, EmpreendimentoStatus, ArquivoTipo


# --- Modelos das Tabelas (Atualizados para usar String) ---

class Imobiliaria(Base):
    __tablename__ = "imobiliarias"
    id = Column(Integer, primary_key=True, index=True)
    imob_nome = Column(String(255), nullable=False)
    imob_creci_juridico = Column(String(50), unique=True, index=True)
    imob_logo_url = Column(String(255), nullable=True)
    status = Column(String(50), default=ImobiliariaStatus.pendente) # MUDANÇA: Enum -> String
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
    permissao = Column(String(50), default=UsuarioPermissao.usuario) # MUDANÇA: Enum -> String
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    imobiliaria = relationship("Imobiliaria", back_populates="usuarios")

class Empreendimento(Base):
    __tablename__ = "empreendimentos"
    id = Column(Integer, primary_key=True, index=True)
    imobiliaria_id = Column(Integer, ForeignKey("imobiliarias.id"), nullable=False)
    emp_nome = Column(String(255), nullable=False)
    emp_apelido = Column(String(255), nullable=True)
    emp_status = Column(String(50), nullable=False) # MUDANÇA: Enum -> String
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
    tipo = Column(String(50), nullable=False) # MUDANÇA: Enum -> String
    link_arquivo = Column(String(255), nullable=False)
    ordem = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    empreendimento = relationship("Empreendimento", back_populates="arquivos")
