#!/bin/bash
# Fichier de test des opérations CRUD pour HBnB API
# Usage: ./api_tests.sh 
# Ou exécutez les commandes individuellement

# ============= CONFIGURATION =============
API_URL="http://localhost:5000/api/v1"
# Ces variables seront remplies durant l'exécution
TOKEN=""
ADMIN_TOKEN=""
USER_ID=""
PLACE_ID=""
REVIEW_ID=""
AMENITY_ID=""

echo "===== TESTS API HBNB ====="

# ============= USER API =============
echo -e "\n===== USER OPERATIONS ====="

# Register a new user
echo -e "\n----- CREATE USER -----"
curl -X POST "$API_URL/users" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "Password123"
  }'

# Register an admin user (if needed for testing)
echo -e "\n----- CREATE ADMIN USER -----"
curl -X POST "$API_URL/users" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Admin",
    "last_name": "User",
    "email": "admin@example.com",
    "password": "AdminPass123"
  }'

# Login as regular user to get token
echo -e "\n----- LOGIN USER -----"
curl -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "Password123"
  }'
# Copy the token from the response and set it as TOKEN variable

# Login as admin user to get admin token
echo -e "\n----- LOGIN ADMIN -----"
curl -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "AdminPass123"
  }'
# Copy the token from the response and set it as ADMIN_TOKEN variable

# --------- Set your tokens here ---------
TOKEN="your_user_token_here"
ADMIN_TOKEN="your_admin_token_here"
USER_ID="your_user_id_here"  # Get from registration or user listing

# Get user profile
echo -e "\n----- GET USER PROFILE -----"
curl -X GET "$API_URL/users/me" \
  -H "Authorization: Bearer $TOKEN"

# Get user by ID
echo -e "\n----- GET USER BY ID -----"
curl -X GET "$API_URL/users/$USER_ID" \
  -H "Authorization: Bearer $TOKEN"

# Update user profile
echo -e "\n----- UPDATE USER -----"
curl -X PUT "$API_URL/users/$USER_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John Updated",
    "last_name": "Doe Updated"
  }'

# List all users (admin only)
echo -e "\n----- LIST ALL USERS (ADMIN ONLY) -----"
curl -X GET "$API_URL/users" \
  -H "Authorization: Bearer $ADMIN_TOKEN"


# ============= PLACE API =============
echo -e "\n\n===== PLACE OPERATIONS ====="

# Create a place
echo -e "\n----- CREATE PLACE -----"
curl -X POST "$API_URL/places" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Beach House",
    "description": "Beautiful oceanfront property",
    "price": 150.00,
    "latitude": 43.2951,
    "longitude": 5.3860
  }'
# Copy the place ID from the response

# --------- Set place ID here ---------
PLACE_ID="your_place_id_here"

# List all places
echo -e "\n----- LIST ALL PLACES -----"
curl -X GET "$API_URL/places"

# Get place by ID
echo -e "\n----- GET PLACE BY ID -----"
curl -X GET "$API_URL/places/$PLACE_ID"

# Update place
echo -e "\n----- UPDATE PLACE -----"
curl -X PUT "$API_URL/places/$PLACE_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 175.00,
    "description": "Updated oceanfront property with new amenities"
  }'

# Delete place
echo -e "\n----- DELETE PLACE -----"
curl -X DELETE "$API_URL/places/$PLACE_ID" \
  -H "Authorization: Bearer $TOKEN"


# ============= AMENITY API =============
echo -e "\n\n===== AMENITY OPERATIONS ====="

# Create amenity (admin only)
echo -e "\n----- CREATE AMENITY (ADMIN ONLY) -----"
curl -X POST "$API_URL/amenities" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Swimming Pool"
  }'
# Copy the amenity ID from the response

# --------- Set amenity ID here ---------
AMENITY_ID="your_amenity_id_here"

# List all amenities
echo -e "\n----- LIST ALL AMENITIES -----"
curl -X GET "$API_URL/amenities"

# Get amenity by ID
echo -e "\n----- GET AMENITY BY ID -----"
curl -X GET "$API_URL/amenities/$AMENITY_ID"

# Update amenity (admin only)
echo -e "\n----- UPDATE AMENITY (ADMIN ONLY) -----"
curl -X PUT "$API_URL/amenities/$AMENITY_ID" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Heated Swimming Pool"
  }'

# Delete amenity (admin only)
echo -e "\n----- DELETE AMENITY (ADMIN ONLY) -----"
curl -X DELETE "$API_URL/amenities/$AMENITY_ID" \
  -H "Authorization: Bearer $ADMIN_TOKEN"


# ============= REVIEW API =============
echo -e "\n\n===== REVIEW OPERATIONS ====="

# Create a review for a place
echo -e "\n----- CREATE REVIEW -----"
curl -X POST "$API_URL/places/$PLACE_ID/reviews" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Amazing stay, very comfortable and great location!",
    "rating": 5
  }'
# Copy the review ID from the response

# --------- Set review ID here ---------
REVIEW_ID="your_review_id_here"

# List all reviews for a place
echo -e "\n----- LIST REVIEWS FOR PLACE -----"
curl -X GET "$API_URL/places/$PLACE_ID/reviews"

# Get review by ID
echo -e "\n----- GET REVIEW BY ID -----"
curl -X GET "$API_URL/reviews/$REVIEW_ID"

# Update review
echo -e "\n----- UPDATE REVIEW -----"
curl -X PUT "$API_URL/reviews/$REVIEW_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Great stay but a bit noisy at night",
    "rating": 4
  }'

# Delete review
echo -e "\n----- DELETE REVIEW -----"
curl -X DELETE "$API_URL/reviews/$REVIEW_ID" \
  -H "Authorization: Bearer $TOKEN"

echo -e "\n\nAPI testing complete!"