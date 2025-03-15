from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade, HBnBFacade  # Correction here (lowercase n)
from http import HTTPStatus

api = Namespace('reviews', description='Review operations')

# Add this function at the beginning of the file, after the imports

def format_review_response(review):
    """Format a review object as a response dictionary with detailed information"""
    # Base response that always works
    response = {
        'id': review.id,
        'text': review.text,
        'rating': review.rating,
        'place_id': review.place_id,
        'user_id': review.user_id,
        'created_at': str(review.created_at)
    }
    
    # Add updated_at if available
    if hasattr(review, 'updated_at'):
        response['updated_at'] = str(review.updated_at)
    
    # Add place details - direct retrieval via facade if necessary
    place_info = {'id': review.place_id}
    try:
        # Try accessing via relationship
        place = getattr(review, 'place', None)
        
        # If relationship doesn't exist or access fails, retrieve via facade
        if not place:
            place = facade.get_place_by_id(review.place_id)
            
        if place:
            # Retrieve basic attributes that all places should have
            place_info['id'] = place.id
            
            # Try to get other useful attributes
            if hasattr(place, 'title'):
                place_info['title'] = place.title
            if hasattr(place, 'name'):
                place_info['name'] = place.name
            if hasattr(place, 'description'):
                desc = place.description
                place_info['description'] = (desc[:100] + '...') if len(desc) > 100 else desc
            if hasattr(place, 'price_per_night'):
                place_info['price'] = place.price_per_night
            if hasattr(place, 'address'):
                place_info['address'] = place.address
            
            response['place'] = place_info
    except Exception as e:
        print(f"Error adding place details: {str(e)}")
        response['place'] = place_info  # Always include at least the ID
    
    # Add user details - direct retrieval via facade if necessary
    user_info = {'id': review.user_id}
    try:
        # Try accessing via relationship
        user = getattr(review, 'user', None)
        
        # If relationship doesn't exist or access fails, retrieve via facade
        if not user:
            user = facade.get_user_by_id(review.user_id)
            
        if user:
            # Retrieve basic attributes that all users should have
            user_info['id'] = user.id
            
            # Try to get other useful attributes
            if hasattr(user, 'first_name'):
                user_info['first_name'] = user.first_name
            if hasattr(user, 'last_name'):
                user_info['last_name'] = user.last_name
            if hasattr(user, 'email'):
                user_info['email'] = user.email
            
            response['user'] = user_info
    except Exception as e:
        print(f"Error adding user details: {str(e)}")
        response['user'] = user_info  # Always include at least the ID
    
    return response

# Define the review model for input validation
review_model = api.model('Review', {
    'place_id': fields.String(required=True, description='ID of the place being reviewed'),
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating (1-5)', min=1, max=5)
})

# Define the review update model (without place_id)
review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(required=False, description='Review text'),
    'rating': fields.Integer(required=False, description='Rating (1-5)', min=1, max=5)
})

# Define the review response model
review_response = api.model('ReviewResponse', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating (1-5)'),
    'place_id': fields.String(description='ID of the place being reviewed'),
    'user_id': fields.String(description='ID of the user who wrote the review'),
    'created_at': fields.String(description='Creation date'),
    'updated_at': fields.String(description='Last update date')
})

@api.route('/')
class ReviewList(Resource):
    @api.doc('list_reviews')
    @api.response(200, 'Success - List of all reviews')
    def get(self):
        """Get all reviews"""
        reviews = facade.get_all_reviews()
        return [format_review_response(review) for review in reviews], HTTPStatus.OK

    @api.doc('create_review')
    @api.expect(review_model)
    @jwt_required()
    def post(self):
        """Create a new review (requires authentication)"""
        try:
            # Get user identity (sub)
            user_id = get_jwt_identity()
            
            # Get complete JWT claims to access is_admin
            jwt_claims = get_jwt()
            is_admin = jwt_claims.get('is_admin', False)
            
            # Get the review data from the request
            data = request.json
            place_id = data.get('place_id', '')
            
            # ADDITION: Check if the user has already left a review for this place
            from app.models.review import Review
            existing_review = Review.query.filter_by(
                user_id=user_id,
                place_id=place_id
            ).first()
            
            if existing_review:
                return {
                    'error': 'You have already left a review for this place. Use PUT to modify it.'
                }, HTTPStatus.CONFLICT
            
            # IMPORTANT MODIFICATION: Check or temporarily create a user
            from app.models.user import User
            from app import db
            
            # Look for the JWT token user in the database
            user = User.query.get(user_id)
            if not user:
                # User doesn't exist, create a temporary one
                print(f"User {user_id} does not exist, creating temporary user")
                new_user = User(
                    id=user_id,
                    email=f"auto_{user_id[:8]}@example.com",
                    first_name="Temporary",
                    last_name="User"
                )
                db.session.add(new_user)
                db.session.commit()
                user = new_user
            
            # Create review with all required fields
            review_data = {
                'text': data.get('text', ''),
                'rating': data.get('rating', 5),
                'place_id': place_id,
                'user_id': user_id  # Directly include user ID in the data
            }
            
            # Simplified call to facade method
            review = facade.create_review(review_data)
            
            # Return the created review with enriched data
            return format_review_response(review), HTTPStatus.CREATED
            
        except ValueError as e:
            return {'error': str(e)}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            import traceback
            print(traceback.format_exc())
            
            # ADDITION: Specific handling for unique constraint error
            if 'unique_user_place_review' in str(e):
                return {
                    'error': 'You have already left a review for this place. Use PUT to modify it.'
                }, HTTPStatus.CONFLICT
                
            return {'error': f"Unexpected error: {str(e)}"}, HTTPStatus.INTERNAL_SERVER_ERROR

@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    @api.doc('get_review')
    @api.response(200, 'Success', review_response)
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get a review by ID"""
        review = facade.get_review_by_id(review_id)
        if not review:
            return {'error': 'Review not found'}, HTTPStatus.NOT_FOUND
            
        return format_review_response(review), HTTPStatus.OK

    @api.doc('update_review')
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    @api.response(403, 'Forbidden - Not the author')
    @api.response(404, 'Review not found')
    @jwt_required()
    def put(self, review_id):
        """Update a review (author or admin only)"""
        # Get user identity (sub)
        user_id = get_jwt_identity()
        
        # Get complete JWT claims to access is_admin
        jwt_claims = get_jwt()
        is_admin = jwt_claims.get('is_admin', False)
        
        print(f"DEBUG - Update method: User ID: {user_id}, Is Admin: {is_admin}")
        
        # Get review and check if it exists
        review = facade.get_review_by_id(review_id)
        if not review:
            return {'error': 'Review not found'}, HTTPStatus.NOT_FOUND
        
        # Check authorship or admin status before allowing update
        if review.user_id != user_id and not is_admin:
            return {'error': 'You must be the author or an admin to update this review'}, HTTPStatus.FORBIDDEN
            
        # Process the update (admins can update any review)
        try:
            review_data = api.payload
            updated_review = facade.update_review(review_id, review_data)
            
            # Return the updated review with enriched data
            return format_review_response(updated_review), HTTPStatus.OK
        except ValueError as e:
            return {'error': str(e)}, HTTPStatus.BAD_REQUEST
    
    @api.doc('delete_review')
    @api.response(204, 'Review deleted successfully')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    @api.response(403, 'Forbidden - Not the author')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review (author or admin only)"""
        # Get user identity (sub)
        user_id = get_jwt_identity()
        
        # Get complete JWT claims to access is_admin
        jwt_claims = get_jwt()
        is_admin = jwt_claims.get('is_admin', False)
        
        print(f"DEBUG - Delete method: User ID: {user_id}, Is Admin: {is_admin}")
        
        # Get review and check if it exists
        review = facade.get_review_by_id(review_id)
        if not review:
            return {'error': 'Review not found'}, HTTPStatus.NOT_FOUND
        
        # Check authorship or admin status before allowing deletion
        if review.user_id != user_id and not is_admin:
            return {'error': 'You must be the author or an admin to delete this review'}, HTTPStatus.FORBIDDEN
            
        # Delete the review (admins can delete any review)
        try:
            # IMPORTANT: Pass current user ID as second parameter
            result = facade.delete_review(review_id, user_id)
            if result:
                return '', HTTPStatus.NO_CONTENT
            else:
                return {'error': 'Failed to delete review'}, HTTPStatus.BAD_REQUEST
        except ValueError as e:
            return {'error': str(e)}, HTTPStatus.BAD_REQUEST
