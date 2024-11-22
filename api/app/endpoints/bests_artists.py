from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from fonctions.bigquery_connection import connection_bigquery
from fonctions.pagination import paginate

router = APIRouter()

@router.get("/bests_artists")
def get_bests_artists(
    show: bool = Query(True, description="True pour inclure les show, False sinon"),
    followers: bool = Query(True, description="True pour inclure les followers, False sinon"),
    page: int = 1,
    lim: int = 10
):
    """
    Récupère les meilleurs artistes, trié en fonction de 2 variables au choix : 
    le nombre de futurs show et le nombre de followers de l'artiste sur le site badsintown.com

    Args:
        show (bool) : Inclure les show dans le trie (par défaut : True).
        followers (bool) : Inclure les followers dans le trie (par défaut : True).
        page (int): Numéro de la page (par défaut : 1).
        lim (int): Nombre d'événements par page (par défaut : 10).

    Returns:
        dict: Liste des artistes les plus populaires en fonction de leur nombre de futures show 
        et/ou leur nombre de followers.
    """

    # Construction de la requête SQL
    
    if show and followers:
        query = f"""
        SELECT
            artistName,
            show,
            followers

        FROM
            `ai-technologies-ur2.dataset_groupe_2.test`
        ORDER BY show DESC, followers DESC
        """
        
    elif show and not followers:
        query = f"""
        SELECT
            artistName,
            show,
            followers

        FROM
            `ai-technologies-ur2.dataset_groupe_2.test`
        ORDER BY show DESC
        """
    
    elif followers and not show:
        query = f"""
        SELECT
            artistName,
            show,
            followers

        FROM
            `ai-technologies-ur2.dataset_groupe_2.test`
        ORDER BY followers DESC
        """
    
    else :
        query = f"""
        SELECT
            artistName,
            show,
            followers

        FROM
            `ai-technologies-ur2.dataset_groupe_2.test`
        """
        
    # Exécution de la requête et gestion des exceptions
    try:
        results = connection_bigquery(query)
        # Paginer les résultats
        return paginate(results, page, lim)
    except Exception as e:
        return {"success": False, "error": str(e)}
