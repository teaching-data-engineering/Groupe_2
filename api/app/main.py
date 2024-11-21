from fastapi import FastAPI
from typing import Union

# http://127.0.0.1:8000/docs
# Permet de tester tous les endpoints directement depuis cette interface


app = FastAPI()

@app.get("/")       # Exécute la fonction qui est en dessous
def read_root():
    return {"Hello": "World"}

@app.get("/mon_endpoint/{objet_id}")    # Construit un endpoint=URL
async def read_objet(objet_id: int, q: Union[str, None] = None):
    return {"objet_id": objet_id, "q": q}

# Création d'un endpoint PUT
from pydantic import BaseModel

class Objet(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.put("/mon_endpoint/{objet_id}")  # Met a jour des ressources existantes (ex : MDP oublié)
def update_objet(objet_id: int, objet: Objet):  # objet_id = parametre d'URL
    return {"objet_name": objet.name, "objet_id": objet_id}



# Sécurisation de l'API avec un Token
from fastapi import HTTPException, Header, Depends, FastAPI
from typing import Annotated

# Impoort des tokens et keys
import json
with open('api/app/config.json') as file:
    config = json.load(file)

# Récupération des tokens et des keys
AUTHORIZED_TOKENS = config["tokens"]
AUTHORIZED_KEYS = config["keys"]

# Fonction de vérification de token
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token not in AUTHORIZED_TOKENS:
        raise HTTPException(status_code=403, detail="Token invalide")

async def verify_key(x_key: Annotated[str, Header()]):
    if x_key not in AUTHORIZED_KEYS:
        raise HTTPException(status_code=403, detail="Clé invalide")

@app.get("/secure-endpoint", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]

