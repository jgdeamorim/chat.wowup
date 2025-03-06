from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """
    Base para o modelo de usuários.
    """
    username: str
    email: EmailStr
    role: str  # Pode ser "admin", "user", "viewer"

class UserCreate(UserBase):
    """
    Modelo de criação de usuários.
    """
    password: str  # Necessário apenas para registro

class UserDB(UserBase):
    """
    Modelo armazenado no banco de dados.
    """
    id: Optional[str]
    hashed_password: str
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime]
