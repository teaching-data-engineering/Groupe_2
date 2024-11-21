
# Ce ficheir enverra des requetes à l'API pour tester son fonctionnement

import requests

# URL de l'API
base_url = "http://127.0.0.1:8000"

# Token et clé autorisés
headers = {
    "x_token": "token_securise",  # Token valide
    "x_key": "key_securise"      # Clé valide
}

# Tester l'endpoint racine
response = requests.get(f"{base_url}/")
print("Endpoint racine :", response.json())

# Tester un endpoint dynamique
response = requests.get(f"{base_url}/mon_endpoint/42?q=test")
print("Endpoint dynamique :", response.json())

# Tester l'endpoint sécurisé
response = requests.get(f"{base_url}/secure-endpoint", headers=headers)
print("Endpoint sécurisé :", response.json())