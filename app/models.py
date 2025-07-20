from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, text
from .database import Base
import enum

class ImobiliariaStatus(str, enum.Enum):
    ativo = "ativo"
    inativo = "inativo"
    pendente = "pendente"

class Imobiliaria(Base):
    __tablename__ = "imobiliarias"

    id = Column(Integer, primary_key=True, index=True)
    imob_nome = Column(String(255), nullable=False)
    imob_creci_juridico = Column(String(50), unique=True, index=True)
    imob_logo_url = Column(String(255), nullable=True)
    status = Column(Enum(ImobiliariaStatus), default=ImobiliariaStatus.pendente)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
