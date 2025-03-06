import pytest
from httpx import AsyncClient
from app.main import app  # Certifique-se de importar a instância do FastAPI

# Para utilizar async com pytest, marque os testes com o decorator pytest.mark.asyncio
@pytest.mark.asyncio
async def test_register_user():
    payload = {
        "username": "testuser",
        "email": "testuser@example.com",
        "role": "user",
        "password": "securepassword"
    }

    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post("/users/register", json=payload)
    
    assert response.status_code == 200
    assert response.json() == {"response": "Usuário registrado com sucesso!"}


@pytest.mark.asyncio
async def test_login_user():
    payload = {
        "email": "testuser@example.com",
        "password": "securepassword"
    }

    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post("/users/login", data=payload)
    
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_list_users():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get("/users/")

    assert response.status_code == 200
    assert isinstance(response.json()['users'], list)


@pytest.mark.asyncio
async def test_get_system_status():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get("/admin/system-status")

    assert response.status_code == 200
    assert "system_status" in response.json()


@pytest.mark.asyncio
async def test_create_module():
    payload = {
        "module_name": "new_module"
    }

    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post("/chat/create-module", json=payload)

    assert response.status_code == 200
    assert "Módulo 'new_module' criado com sucesso!" in response.json()['message']


@pytest.mark.asyncio
async def test_deploy_status():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get("/deploy/status")
    
    assert response.status_code == 200
    assert "deploy_status" in response.json()


@pytest.mark.asyncio
async def test_frontend_sync():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post("/frontend-sync/sync")
    
    assert response.status_code == 200
    assert "Sincronização do frontend iniciada com sucesso!" in response.json()['message']


# Adicionar outros testes para outros endpoints conforme necessário
@pytest.mark.asyncio
async def test_update_user():
    payload = {
        "email": "testuser@example.com",
        "new_username": "updateduser"
    }

    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.put("/users/update", json=payload)

    assert response.status_code == 200
    assert response.json() == {"response": "Usuário atualizado com sucesso!"}


@pytest.mark.asyncio
async def test_delete_user():
    payload = {
        "email": "testuser@example.com"
    }

    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.delete("/users/delete", json=payload)

    assert response.status_code == 200
    assert response.json() == {"response": "Usuário removido com sucesso!"}
