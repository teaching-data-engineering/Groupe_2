from fastapi import APIRouter, HTTPException
from datetime import datetime
from fonctions.bigquery_connection import connection_bigquery
from fonctions.pagination import paginate

router = APIRouter()

@router.get("/event_on_hour")
def get_event_on_hour(
    date: str,
    start_hour: str,
    page: int = 1,
    lim: int = 10
):
    """
    Récupère les événements ayant lieu à partir d'une certaine heure pour une journée spécifique.

    Args:
        date (str): La date sous le format 'YYYY-MM-DD'.
        start_hour (str): L'heure de début à partir de laquelle les événements doivent être récupérés (format : 'HH:MM').
        page (int): Numéro de la page (par défaut : 1).
        lim (int): Nombre d'événements par page (par défaut : 10).

    Returns:
        dict: Liste des événements ayant lieu après l'heure spécifiée pour la date donnée.
    """
    # Vérification du format de `date`
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Expected format: YYYY-MM-DD")

    # Vérification du format de `start_hour`
    try:
        datetime.strptime(start_hour, '%H:%M')
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid start_hour format. Expected format: HH:MM")

    # Construction de la requête SQL pour récupérer les événements à partir de la date et de l'heure spécifiées
    query = f"""
    SELECT 
        FORMAT_DATETIME('%Y-%m-%dT%H:%M:%S', startsAt) AS event_datetime,
        venueName,
        artistName,
        title,
        locationText,
        rsvpCountInt,
        startsAt,
        event_duration,
        popularity
        
    FROM 
        `ai-technologies-ur2.dataset_groupe_2.test`
    WHERE 
        FORMAT_DATETIME('%Y-%m-%d', startsAt) = '{date}' 
        AND FORMAT_DATETIME('%H:%M', startsAt) >= '{start_hour}'
    ORDER BY event_datetime ASC
    """

    # Exécution de la requête et gestion des exceptions
    try:
        results = connection_bigquery(query)
        # Paginer les résultats
        return paginate(results, page, lim)
    except Exception as e:
        return {"success": False, "error": str(e)}
