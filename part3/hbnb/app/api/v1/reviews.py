from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade
from http import HTTPStatus

api = Namespace('reviews', description='Review operations')

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
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'place_id': review.place_id,
            'user_id': review.user_id,
            'created_at': str(review.created_at),
            'updated_at': str(review.updated_at)
        } for review in reviews], HTTPStatus.OK

    @api.doc('create_review')
    @api.expect(review_model)
    @api.response(201, 'Review created successfully', review_response)
    @api.response(400, 'Invalid input or review constraints not met')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    @api.response(404, 'Place not found')
    @jwt_required()
    def post(self):
        """Create a new review (requires authentication)"""
        # Get the current user's identity from the JWT token
        current_user = get_jwt_identity()
        user_id = current_user['id']
        
        # Get the review data from the request
        data = request.json
        place_id = data.get('place_id')
        
        # Validate place exists
        place = facade.get_place_by_id(place_id)
        if not place:
            return {'error': 'Place not found'}, HTTPStatus.NOT_FOUND
        
        # Check constraint 1: Users cannot review their own places
        if place.owner_id == user_id:
            return {'error': 'You cannot review your own place'}, HTTPStatus.BAD_REQUEST
        
        # Check constraint 2: Users can only leave one review per place
        existing_reviews = facade.get_reviews_by_place(place_id)
        for review in existing_reviews:
            if review.user_id == user_id:
                return {'error': 'You have already reviewed this place'}, HTTPStatus.BAD_REQUEST
        
        # Add user_id to the review data
        data['user_id'] = user_id
        
        try:
            # Create the review
            review = facade.create_review(data)
            
            # Return the created review
            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'place_id': review.place_id,
                'user_id': review.user_id,
                'created_at': str(review.created_at),
                'updated_at': str(review.updated_at)
            }, HTTPStatus.CREATED
            
        except ValueError as e:
            return {'error': str(e)}, HTTPStatus.BAD_REQUEST

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
            
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'place_id': review.place_id,
            'user_id': review.user_id,
            'created_at': str(review.created_at),
            'updated_at': str(review.updated_at)
        }, HTTPStatus.OK

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
        # Get current user from token
        current_user = get_jwt_identity()
        user_id = current_user.get('id')
        is_admin = current_user.get('is_admin', False)
        
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
            
            # Return the updated review
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                # Add other fields as needed
                'updated_at': updated_review.updated_at.isoformat()
            }, HTTPStatus.OK
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
        # Get current user from token
        current_user = get_jwt_identity()
        user_id = current_user.get('id')
        is_admin = current_user.get('is_admin', False)
        
        # Get review and check if it exists
        review = facade.get_review_by_id(review_id)
        if not review:
            return {'error': 'Review not found'}, HTTPStatus.NOT_FOUND
        
        # Check authorship or admin status before allowing deletion
        if review.user_id != user_id and not is_admin:
            return {'error': 'You must be the author or an admin to delete this review'}, HTTPStatus.FORBIDDEN
            
        # Delete the review (admins can delete any review)
        try:
            facade.delete_review(review_id)
            return '', HTTPStatus.NO_CONTENT
        except ValueError as e:
            return {'error': str(e)}, HTTPStatus.BAD_REQUEST
