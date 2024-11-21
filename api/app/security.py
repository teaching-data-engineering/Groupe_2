# security.py
from fastapi import HTTPException, Header
from typing import Annotated
import json

# Chargement des tokens depuis le fichier config.json
try:
    with open('api/app/config.json') as file:
        config = json.load(file)
except FileNotFoundError:
    raise RuntimeError("Le fichier 'config.json' est introuvable.")
except json.JSONDecodeError:
    raise RuntimeError("Le fichier 'config.json' est mal formé.")

# Récupération des tokens depuis le fichier config.json
tokens = config["tokens"]

# Fonction de vérification des tokens
async def verify_token(x_token: Annotated[str, Header(alias="Clé d'accès")]):
    if x_token not in tokens:
        raise HTTPException(status_code=403, detail="Token invalide")
    return x_token