# ...existing code...

def get_place_by_id(self, place_id):
    """
    Récupère un lieu par son ID
    
    Args:
        place_id (str): L'ID du lieu à récupérer
        
    Returns:
        Place ou None: L'objet Place s'il est trouvé, None sinon
    """
    from app.models.place import Place
    
    # Version simplifiée sans relations
    try:
        return Place.query.get(place_id)
    except Exception:
        return None

def get_review_by_id(self, review_id):
    """
    Récupère un avis par son ID
    
    Args:
        review_id (str): L'ID de l'avis à récupérer
        
    Returns:
        Review ou None: L'objet Review s'il est trouvé, None sinon
    """
    from app.models.review import Review
    
    # Version simplifiée sans relations
    try:
        return Review.query.get(review_id)
    except Exception:
        return None
