from google.cloud import bigquery
from google.oauth2 import service_account

def connection_bigquery(query: str):
    """
    Connexion à BigQuery et exécution de la requête SQL.
    
    Args:
        query (str): Requête SQL à exécuter.
    
    Returns:
        list: Résultats sous forme de liste de dictionnaires.
    """
    credentials = service_account.Credentials.from_service_account_file(
        "api/app/sa-key-group-2.json"
    )
    client = bigquery.Client(credentials=credentials)
    query_job = client.query(query)
    results = query_job.result()
    return [dict(row) for row in results]
