from fastapi import APIRouter, Query, Depends
from fonctions.bigquery_connection import connection_bigquery
from fonctions.pagination import paginate
from security import verify_token


router = APIRouter()

@router.get("/events_search_rsvp_day_venue", dependencies=[Depends(verify_token("event_search"))])
def get_rsvp_day_venue(page: int = 1, lim: int = 10, order_date: int = 1, order_nb_event: int = 1):
    """
    Endpoint pour récupérer les événements avec RSVP, groupés par jour et lieu.
    
    Args:
        page (int): Numéro de la page pour la pagination.
        lim (int): Nombre d'éléments par page.
        order_date (int): Ordre pour les dates (1 pour DESC, autre pour ASC).
        order_nb_event (int): Ordre pour les RSVP (1 pour DESC, autre pour ASC).
    
    Returns:
        dict: Résultats paginés avec les événements triés.
    """
    # Conversion des paramètres d'ordre en texte SQL
    order_date = 'DESC' if int(order_date) == 1 else 'ASC'
    order_nb_event = 'DESC' if int(order_nb_event) == 1 else 'ASC'

    query = f"""
        SELECT DATE(startsAt) AS Date, venueName, COUNT(rsvpCountInt) AS rsvp 
        FROM ai-technologies-ur2.dataset_groupe_2.test 
        GROUP BY venueName, DATE(startsAt)
        ORDER BY Date {order_date}, rsvp {order_nb_event}
    """
    
    # Exécution de la requête et gestion des exceptions
    try:
        results = connection_bigquery(query)
        return paginate(results, page, lim)
    except Exception as e:
        return {"success": False, "error": str(e)}
