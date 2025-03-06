from fastapi import APIRouter, HTTPException
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.database import get_database
from app.models.user_model import UserCreate, UserDB
from datetime import datetime
import logging

# Configuração de logs
logger = logging.getLogger("users")
logger.setLevel(logging.INFO)

router = APIRouter()

@router.post("/register", summary="Registra um novo usuário")
async def register_user(user: UserCreate):
    """
    Registra um novo usuário no sistema.
    """
    db = await get_database()

    if db is None:
        logger.error("❌ Erro ao conectar ao banco de dados.")
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")

    # Verifica se a coleção 'users' existe
    collections = await db.list_collection_names()
    if "users" not in collections:
        logger.warning("⚠️ Criando coleção 'users' no MongoDB...")
        await db.create_collection("users")

    # Verifica se o usuário já está cadastrado
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado.")

    # Garante que a senha seja devidamente hashada antes de salvar no banco
    hashed_password = await get_password_hash(user.password)

    # Criando o objeto de dados do usuário para salvar no banco de dados
    user_data = UserDB(
        username=user.username,
        email=user.email,
        role=user.role,
        hashed_password=hashed_password,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    ).dict(exclude_unset=True)  # Exclui os campos não definidos, como o id

    try:
        # Insere o usuário na coleção 'users'
        await db["users"].insert_one(user_data)
        logger.info(f"✅ Novo usuário registrado: {user.email}")
        return {"response": "Usuário registrado com sucesso!"}
    except Exception as e:
        logger.error(f"❌ Erro ao registrar o usuário: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao registrar o usuário: {str(e)}")

