# app/models/user_model.py

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class User(BaseModel):
    """
    Modelo de dados para usuários.
    """
    id: Optional[str]
    username: str
    email: EmailStr
    hashed_password: str
    role: str  # admin, user, viewer
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime]
