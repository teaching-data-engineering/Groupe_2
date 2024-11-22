from fastapi import APIRouter, Query
from fonctions.bigquery_connection import connection_bigquery
from fonctions.pagination import paginate
from typing import Union
from fastapi import Depends
from security import verify_token

router = APIRouter()

@router.get("/event_by_day_of_week", dependencies=[Depends(verify_token("event_by_day_of_week"))])
def get_events_by_day(
    week: Union[int, None] = Query(None, description="Numéro de la semaine (facultatif)"),
    order_date: int = Query(1, description="1 pour tri décroissant, 0 pour tri croissant"),
    page: int = Query(1, description="Numéro de la page"),
    lim: int = Query(10, description="Nombre d'événements par page")
):
    """
    Récupère les événements par jour de la semaine avec un tri et un filtrage optionnel.

    Args:
        week (Union[int, None]): Filtrer par numéro de semaine (par défaut : None).
        order_date (int): Ordre de tri des dates, 1 pour décroissant (par défaut), 0 pour croissant.
        page (int): Numéro de la page (par défaut : 1).
        lim (int): Nombre d'événements par page (par défaut : 10).

    Returns:
        dict: Résultats paginés des événements.
    """

    # Définir l'ordre de tri
    order = "DESC" if order_date == 1 else "ASC"

    # Construire le filtre pour la requête SQL
    filter_req = f"WHERE num_semaine = {week}" if week else ""

    # Construire la requête SQL
    query = f"""
        SELECT 
            DATE(startsAt) AS event_date, 
            COUNT(title) AS total_events 
        FROM 
            `ai-technologies-ur2.dataset_groupe_2.test`
        {filter_req}
        GROUP BY 
            event_date
        ORDER BY 
            event_date {order}
    """

    # Exécution de la requête et gestion des exceptions
    try:
        results = connection_bigquery(query)
        return paginate(results, page, lim)
    except Exception as e:
        return {"success": False, "error": str(e)}
