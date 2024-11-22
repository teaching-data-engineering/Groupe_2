from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from fonctions.bigquery_connection import connection_bigquery
from fonctions.pagination import paginate
from security import verify_token  # Import de la fonction de vérification des tokens

router = APIRouter()

@router.get("/event_loc/{start_date}", dependencies=[Depends(verify_token("event_loc"))])
def get_event_loc(
    start_date: str, 
    page: int = 1, 
    lim: int = 10, 
    last_date: str = None, 
    order_number_event: int = 1, 
    order_date: int = 0
):
    """
    Endpoint pour récupérer les événements et leurs localisations à partir d'une date donnée.
    """
    # Vérification du format de `start_date`
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid start_date format. Expected format: YYYY-MM-DD")

    # Vérification du format de `last_date` si fourni
    if last_date:
        try:
            datetime.strptime(last_date, '%Y-%m-%d')
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid last_date format. Expected format: YYYY-MM-DD")

    # Préparer les options de tri
    order_number_event = "DESC" if order_number_event == 1 else "ASC"
    order_date = "DESC" if order_date == 1 else "ASC"

    # Construction de la requête SQL
    if last_date is None:
        query = f"""
        SELECT 
            FORMAT_DATETIME('%Y-%m-%d', startsAt) AS event_date,
            locationText,
            COUNT(*) AS nombre_event
        FROM 
            `ai-technologies-ur2.dataset_groupe_2.test`
        WHERE 
            FORMAT_DATETIME('%Y-%m-%d', startsAt) = '{start_date}'
        GROUP BY 
            event_date, locationText
        ORDER BY 
            event_date {order_date}, nombre_event {order_number_event};
        """
    else:
        query = f"""
        SELECT 
            FORMAT_DATETIME('%Y-%m-%d', startsAt) AS event_date,
            locationText,
            COUNT(*) AS nombre_event
        FROM 
            `ai-technologies-ur2.dataset_groupe_2.test`
        WHERE 
            FORMAT_DATETIME('%Y-%m-%d', startsAt) BETWEEN '{start_date}' AND '{last_date}' 
        GROUP BY 
            event_date, locationText
        ORDER BY 
            event_date {order_date}, nombre_event {order_number_event};
        """

    # Exécution de la requête et gestion des exceptions
    try:
        results = connection_bigquery(query)
        return paginate(results, page, lim)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))