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
    ).dict()

    # Insere o usuário na coleção 'users'
    await db["users"].insert_one(user_data)
    logger.info(f"✅ Novo usuário registrado: {user.email}")
    return {"response": "Usuário registrado com sucesso!"}

@router.post("/login", summary="Realiza login e retorna um token de acesso")
async def login_user(email: str, password: str):
    """
    Realiza login e retorna um token de acesso.
    """
    db = await get_database()

    if db is None:
        logger.error("❌ Erro ao conectar ao banco de dados.")
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")

    user = await db["users"].find_one({"email": email})
    if not user or not await verify_password(password, user["hashed_password"]):
        logger.warning(f"⚠️ Tentativa de login falha para {email}")
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")

    access_token = await create_access_token(user_id=user["email"], role=user["role"])
    logger.info(f"🔑 Token gerado para {email}")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/", summary="Lista todos os usuários cadastrados")
async def list_users():
    """
    Retorna uma lista de usuários cadastrados.
    """
    try:
        db = await get_database()

        if db is None:
            raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")

        if "users" not in await db.list_collection_names():
            logger.warning("⚠️ Nenhum usuário cadastrado ainda.")
            return {"users": []}

        # Seleciona os dados dos usuários, omitindo a senha
        users = await db["users"].find({}, {"_id": 0, "hashed_password": 0}).to_list(None)
        return {"users": users}

    except Exception as e:
        logger.error(f"❌ Erro ao listar usuários: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar usuários: {str(e)}")
