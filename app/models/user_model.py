from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class User(BaseModel):
    """
    Modelo de dados para usuários.
    """
    id: Optional[str] = None
    username: str
    email: EmailStr
    password: str  # 🔹 Agora está correto para receber a senha antes do hash
    role: str  # admin, user, viewer
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime] = None
