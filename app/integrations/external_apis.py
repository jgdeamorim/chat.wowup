# app/integrations/external_apis.py

import requests
from fastapi import APIRouter, HTTPException
import os

router = APIRouter()

OPENAI_API_KEY = os.getenv("AI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@router.post("/openai")
async def generate_text(prompt: str):
    """
    Envia um prompt para o OpenAI e retorna a resposta gerada.
    """
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    payload = {"model": "gpt-4o", "messages": [{"role": "user", "content": prompt}]}

    response = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao se conectar ao OpenAI.")

    return response.json()

@router.get("/github/repos")
async def list_github_repos():
    """
    Retorna uma lista de repositórios do usuário autenticado no GitHub.
    """
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.get("https://api.github.com/user/repos", headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao obter repositórios do GitHub.")

    return response.json()
