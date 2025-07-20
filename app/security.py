# backend/app/security.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
# MUDANÇA 1: Importar 'database' diretamente para obter o get_db
from . import models, schemas, config, database

# Configuração
settings = config.settings
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# Esquema de autenticação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

# Contexto para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Dependências de Segurança ---

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(database.get_db) # MUDANÇA 2: Corrigido de crud.get_db para database.get_db
):
    # MUDANÇA 3: A importação do crud é feita DENTRO da função para quebrar o ciclo
    from . import crud

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = crud.get_usuario_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

def get_current_admin_user(current_user: models.Usuario = Depends(get_current_user)):
    if current_user.permissao != models.UsuarioPermissao.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Requer privilégios de administrador."
        )
    return current_user
