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
tokens = config["tokens"]  # `tokens` est maintenant un dictionnaire
master_token = config["master_token"]

def verify_token(endpoint: str):
    """
    Retourne une fonction de dépendance qui vérifie si le token ou le master_token est valide pour une route spécifique.
    """
    def verifier(x_token: Annotated[str, Header(alias="Code")]):
        # Vérification que le token est valide pour cet endpoint ou qu'il s'agit du master_token
        if x_token != tokens.get(endpoint) and x_token != master_token:
            raise HTTPException(status_code=403, detail="Mot de passe invalide pour cette route")
        return x_token
    return verifier