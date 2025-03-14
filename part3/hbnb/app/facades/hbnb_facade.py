def get_place_by_id(self, place_id):
    """
    Get a place by its ID
    
    Args:
        place_id (str): The ID of the place to retrieve
        
    Returns:
        Place or None: The Place object if found, None otherwise
    """
    from app.models.place import Place
    
    # Simplified version without relationships
    try:
        return Place.query.get(place_id)
    except Exception:
        return None

def get_reviews_by_place(self, place_id):
    """
    Get all reviews for a specific place
    
    Args:
        place_id (str): The ID of the place to get reviews for
        
    Returns:
        list[Review]: A list of Review objects related to the place, or empty list if none
    """
    from app.models.review import Review
    
    try:
        return Review.query.filter_by(place_id=place_id).all()
    except Exception:
        return []

def get_all_reviews(self):
    """
    Get all reviews
    
    Returns:
        list[Review]: A list of all Review objects
    """
    from app.models.review import Review
    
    try:
        return Review.query.all()
    except Exception:
        return []

def create_review(self, data, current_user_id=None):
    """
    Create a new review
    
    Args:
        data (dict): The data to create the review
        current_user_id (str, optional): The current user ID extracted from JWT token
        
    Returns:
        Review: The created Review object
        
    Raises:
        ValueError: If the data is invalid
    """
    from app.models.review import Review
    from app import db
    
    # Debug
    print(f"DEBUG FACADE - data: {data}, current_user_id: {current_user_id}")
    
    try:
        # Validate required data
        if not data.get('place_id'):
            raise ValueError("L'ID du lieu est requis")
            
        # Use current user ID from JWT token or from data
        user_id = current_user_id or data.get('user_id')
        if not user_id:
            raise ValueError("L'ID utilisateur est manquant")
        
        print(f"DEBUG FACADE - Using user_id: {user_id}")
        
        review = Review(
            text=data.get('text', ''),
            rating=int(data.get('rating', 5)),  # Explicit conversion to int
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
    Update an existing review
    
    Args:
        review_id (str): The ID of the review to update
        data (dict): The new review data
        
    Returns:
        Review: The updated Review object
        
    Raises:
        ValueError: If the data is invalid or the review doesn't exist
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
    Delete a review
    
    Args:
        review_id (str): The ID of the review to delete
        
    Raises:
        ValueError: If the review doesn't exist or cannot be deleted
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
    Get a review by its ID
    
    Args:
        review_id (str): The ID of the review to retrieve
        
    Returns:
        Review or None: The Review object if found, None otherwise
    """
    from app.models.review import Review
    
    # Simplified version without relationships
    try:
        return Review.query.get(review_id)
    except Exception:
        return None
