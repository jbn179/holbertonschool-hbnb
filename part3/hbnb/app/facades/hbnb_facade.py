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

def get_reviews_by_place(self, place_id):
    """
    Récupère tous les avis pour un lieu spécifique
    
    Args:
        place_id (str): L'ID du lieu pour lequel récupérer les avis
        
    Returns:
        list[Review]: Une liste d'objets Review liés au lieu, ou liste vide si aucun
    """
    from app.models.review import Review
    
    try:
        return Review.query.filter_by(place_id=place_id).all()
    except Exception:
        return []

def get_all_reviews(self):
    """
    Récupère tous les avis
    
    Returns:
        list[Review]: Une liste de tous les objets Review
    """
    from app.models.review import Review
    
    try:
        return Review.query.all()
    except Exception:
        return []

def create_review(self, data, current_user_id=None):
    """
    Crée un nouvel avis
    
    Args:
        data (dict): Les données pour créer l'avis
        current_user_id (str, optional): L'ID de l'utilisateur actuel extrait du token JWT
        
    Returns:
        Review: L'objet Review créé
        
    Raises:
        ValueError: Si les données sont invalides
    """
    from app.models.review import Review
    from app import db
    
    # Debug
    print(f"DEBUG FACADE - data: {data}, current_user_id: {current_user_id}")
    
    try:
        # Valider les données requises
        if not data.get('place_id'):
            raise ValueError("L'ID du lieu est requis")
            
        # Utiliser l'ID utilisateur fourni par le token JWT ou celui dans les données
        user_id = current_user_id or data.get('user_id')
        if not user_id:
            raise ValueError("L'ID utilisateur est manquant")
        
        print(f"DEBUG FACADE - Using user_id: {user_id}")
        
        review = Review(
            text=data.get('text', ''),
            rating=int(data.get('rating', 5)),  # Conversion explicite en int
            place_id=data.get('place_id'),
            user_id=user_id
        )
        
        db.session.add(review)
        db.session.commit()
        return review
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Échec de création de l'avis: {str(e)}")

def update_review(self, review_id, data):
    """
    Met à jour un avis existant
    
    Args:
        review_id (str): L'ID de l'avis à mettre à jour
        data (dict): Les nouvelles données de l'avis
        
    Returns:
        Review: L'objet Review mis à jour
        
    Raises:
        ValueError: Si les données sont invalides ou si l'avis n'existe pas
    """
    from app import db
    
    review = self.get_review_by_id(review_id)
    
    if not review:
        raise ValueError("Avis non trouvé")
    
    try:
        if 'text' in data:
            review.text = data['text']
        if 'rating' in data:
            review.rating = data['rating']
        
        db.session.commit()
        return review
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Échec de mise à jour de l'avis: {str(e)}")

def delete_review(self, review_id):
    """
    Supprime un avis
    
    Args:
        review_id (str): L'ID de l'avis à supprimer
        
    Raises:
        ValueError: Si l'avis n'existe pas ou ne peut pas être supprimé
    """
    from app import db
    
    review = self.get_review_by_id(review_id)
    
    if not review:
        raise ValueError("Avis non trouvé")
    
    try:
        db.session.delete(review)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Échec de suppression de l'avis: {str(e)}")

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
