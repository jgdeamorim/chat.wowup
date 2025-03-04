# app/routes/users.py

from fastapi import APIRouter, HTTPException, Depends
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.database import get_database
from app.models.user_model import User
from datetime import timedelta

router = APIRouter()
db = get_database()

@router.post("/register")
async def register_user(user: User):
    """
    Registra um novo usuário no sistema.
    """
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado.")

    user.password = get_password_hash(user.password)
    await db["users"].insert_one(user.dict())
    return {"response": "Usuário registrado com sucesso!"}

@router.post("/login")
async def login_user(email: str, password: str):
    """
    Autentica um usuário e retorna um token JWT.
    """
    user = await db["users"].find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")

    access_token = create_access_token(data={"sub": email}, expires_delta=timedelta(minutes=60))
    return {"access_token": access_token, "token_type": "bearer"}
