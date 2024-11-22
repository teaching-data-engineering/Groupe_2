def paginate(data: list, page: int = 1, lim: int = 10):
    """
    Paginer une liste de dictionnaires.

    Args:
        data (list): Liste de dictionnaires à paginer.
        page (int): Numéro de la page (par défaut : 1).
        lim (int): Nombre d'éléments par page (par défaut : 10).

    Returns:
        dict: Données paginées et métadonnées.
    """
    if not isinstance(data, list):
        raise ValueError("Les données doivent être une liste de dictionnaires.")
    
    total_items = len(data)
    if lim > 100:
        lim = 100
    
    start_index = (page - 1) * lim
    end_index = start_index + lim
    paginated_data = data[start_index:end_index]

    return {
        "data": paginated_data,
        "metadata": {
            "total_items": total_items,
            "total_pages": (total_items + lim - 1) // lim,
            "current_page": page,
            "page_size": lim,
        }
    }
