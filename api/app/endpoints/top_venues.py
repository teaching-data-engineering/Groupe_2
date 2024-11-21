from fastapi import APIRouter, HTTPException, Query
from fonctions.bigquery_connection import connection_bigquery
from fonctions.pagination import paginate

router = APIRouter()

@router.get("/top_venues")
def get_top_venues(
    page: int = 1, 
    lim: int = 10, 
    popularity_filter: str = Query(
        None, 
        regex="^(Very High|High|Medium|Low)$", 
        description="Filtre optionnel pour le niveau de popularité des événements. Valeurs possibles : 'Very High', 'High', 'Medium', 'Low'."
    )
):
    """
    Endpoint pour récupérer les salles avec le plus grand nombre d'événements.

    Args:
        page (int): Numéro de la page à afficher (par défaut : 1).
        lim (int): Nombre d'éléments par page (par défaut : 10).
        popularity_filter (str): Filtre optionnel pour le niveau de popularité ('Very High', 'High', 'Medium', 'Low').

    Returns:
        dict: Données paginées des salles triées par nombre d'événements.
    """
    # Base de la requête SQL
    query = """
    SELECT 
        venueName, 
        COUNT(*) AS event_count
    FROM `ai-technologies-ur2.dataset_groupe_2.test`
    """

    # Ajouter un filtre sur la popularité si spécifié
    if popularity_filter:
        query += f"WHERE popularity = '{popularity_filter}' "

    # Ajouter le groupement et le tri
    query += """
    GROUP BY venueName
    ORDER BY event_count DESC
    """
    
    try:
        # Exécuter la requête SQL pour récupérer les données
        results = connection_bigquery(query)
        # Paginer les résultats
        return paginate(results, page, lim)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))