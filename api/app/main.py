# main.py
from fastapi import FastAPI, Depends, HTTPException
from typing import Union
import json

# Import de la fonction verify_token depuis security.py
from security import verify_token 

# Chargement des tokens depuis le fichier config.json
try:
    with open('api/app/config.json') as file:
        config = json.load(file)
except FileNotFoundError:
    raise RuntimeError("Le fichier 'config.json' est introuvable.")
except json.JSONDecodeError:
    raise RuntimeError("Le fichier 'config.json' est mal formé.")
# Récupération des tokens
tokens = config["tokens"]

# Instance FastAPI
app = FastAPI()

@app.get("/endpoint1", dependencies=[Depends(verify_token)])  # Sécurisé avec token
async def endpoint1(x_token: str = Depends(verify_token)):
    # Définition de la sécurité
    if x_token not in [tokens[0], tokens[1]]:
        raise HTTPException(status_code=403, detail="Accès refusé à Endpoint1")
    return {"message": "Bienvenue sur Endpoint1"}


@app.get("/endpoint2", dependencies=[Depends(verify_token)])  # Sécurisé avec token
async def endpoint2(x_token: str = Depends(verify_token)):
    # Définition de la sécurité
    if x_token not in [tokens[0], tokens[2]]:
        raise HTTPException(status_code=403, detail="Accès refusé à Endpoint2")
    return {"message": "Bienvenue sur Endpoint2"}