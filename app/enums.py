# backend/app/enums.py
import enum

class ImobiliariaStatus(str, enum.Enum):
    ativo = "ativo"
    inativo = "inativo"
    pendente = "pendente"

class UsuarioPermissao(str, enum.Enum):
    superadmin = "superadmin"  # <-- ADICIONADO
    admin = "admin"
    usuario = "usuario"

class EmpreendimentoStatus(str, enum.Enum):
    lancamento = "lancamento"
    em_obras = "em_obras"
    pronto_para_morar = "pronto_para_morar"
    entregue = "entregue"

class ArquivoTipo(str, enum.Enum):
    imagem_fachada = "imagem_fachada"
    imagem_interna = "imagem_interna"
    planta = "planta"
    video = "video"
    tour_360 = "tour_360"
