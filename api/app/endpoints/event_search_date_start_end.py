from fastapi import APIRouter, HTTPException, Depends
from fonctions.bigquery_connection import connection_bigquery
from fonctions.pagination import paginate
from datetime import datetime
from security import verify_token

router = APIRouter()

@router.get("/events_search_h_start_end", dependencies=[Depends(verify_token("events_search_h_start_end"))])
def get_horaire(start_date: str, last_date: str, page: int = 1, lim: int = 10):
    
    # Validation du format des dates
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(last_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Les dates doivent être au format 'YYYY-MM-DD'."
        )
    
    # Construction de la requête SQL
    query = f"""
        SELECT DISTINCT 
            DATE(startsAt) AS day_startsAt,
            TIME(startsAt) AS hour_startsAt, 
            TIME(endsAt) AS hour_endsAt,
            artistName
        FROM ai-technologies-ur2.dataset_groupe_2.test
        WHERE startsAt BETWEEN '{start_date}' AND '{last_date}'
        ORDER BY day_startsAt, hour_startsAt;
    """
    
    # Exécution de la requête et gestion des exceptions
    try:
        results = connection_bigquery(query)
        # Paginer les résultats
        return paginate(results, page, lim)
    except Exception as e:
        return {"success": False, "error": str(e)}
