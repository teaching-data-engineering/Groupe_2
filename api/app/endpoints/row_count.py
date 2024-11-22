from fastapi import APIRouter, HTTPException
from fonctions.bigquery_connection import connection_bigquery
from fonctions.pagination import paginate
from fastapi import Depends
from security import verify_token

router = APIRouter()

@router.get("/row_count/{limit}", dependencies=[Depends(verify_token("row_count"))])
def get_row_count(
    limit: int,
    page: int = 1,
    lim: int = 10
    ):
    """
    Endpoint pour récupérer des données de BigQuery avec pagination.
    
    Args:
        limit (int): Nombre maximum de résultats à récupérer.
        page (int): Numéro de la page à afficher (par défaut : 1).
        lim (int): Nombre d'éléments par page (par défaut : 10).

    Returns:
        dict: Données paginées et métadonnées.
    """
    query = f"""
    SELECT * FROM `ai-technologies-ur2.dataset_groupe_2.test` LIMIT {limit}
    """
    try:
        # Exécuter la requête BigQuery
        results = connection_bigquery(query)
        # Paginer les résultats
        return paginate(results, page, lim)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
