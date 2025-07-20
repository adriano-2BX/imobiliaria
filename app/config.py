# backend/app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Configuração do Banco de Dados
    database_url: str

    # Configuração do JWT
    secret_key: str = "sua_chave_secreta_super_dificil_de_adivinhar"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 # 1 dia

    class Config:
        env_file = ".env"

settings = Settings()
