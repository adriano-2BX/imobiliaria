from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from .models import ImobiliariaStatus

class ImobiliariaBase(BaseModel):
    imob_nome: str
    imob_creci_juridico: Optional[str] = None
    imob_logo_url: Optional[str] = None
    status: ImobiliariaStatus = ImobiliariaStatus.pendente

class ImobiliariaCreate(ImobiliariaBase):
    pass

class Imobiliaria(ImobiliariaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
