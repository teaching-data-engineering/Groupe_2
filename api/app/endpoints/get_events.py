from fastapi import APIRouter
from fonctions.bigquery_connection import connection_bigquery
from fonctions.pagination import paginate

router = APIRouter()

@router.get("/get_events")
def get_events(
    page: int = 1,
    lim: int = 10):
    
    query= """
    SELECT title, venueName
    FROM ai-technologies-ur2.dataset_groupe_2.test
    WHERE ENDS_WITH(locationText,"NY") """
            
    # Exécution de la requête et gestion des exceptions
    try:
        results = connection_bigquery(query)
        # Paginer les résultats
        return paginate(results, page, lim)
    except Exception as e:
        return {"success": False, "error": str(e)}