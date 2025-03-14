#!/bin/bash
# filename: test_relationships.sh

# Script pour tester les relations entre modèles HBnB (User-Place-Review-Amenity)
# Exécuter le script avec: bash test_relationships.sh

# Configuration
API_URL="http://localhost:5000/api/v1"
LOG_FILE="relationship_tests.log"

# Couleurs pour une meilleure lisibilité
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Initialisation
echo "" > $LOG_FILE
echo -e "${BLUE}=== DÉMARRAGE DES TESTS DE RELATIONS HBnB ===${NC}" | tee -a $LOG_FILE
echo -e "Logs complets disponibles dans ${YELLOW}$LOG_FILE${NC}" | tee -a $LOG_FILE
echo "" | tee -a $LOG_FILE

# ---------------------------------------------
# 1. TEST DES UTILISATEURS ET AUTHENTIFICATION
# ---------------------------------------------
echo -e "${BLUE}=== 1. CRÉATION D'UTILISATEUR ET AUTHENTIFICATION ===${NC}" | tee -a $LOG_FILE

echo -e "${GREEN}Création d'un nouvel utilisateur...${NC}" | tee -a $LOG_FILE
USER_RESPONSE=$(curl -s -X POST $API_URL/users \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "securepassword"
  }')

echo "$USER_RESPONSE" >> $LOG_FILE
USER_ID=$(echo "$USER_RESPONSE" | grep -o '"id":"[^"]*' | sed 's/"id":"//')

if [ -z "$USER_ID" ]; then
  echo -e "${RED}ERREUR: ID utilisateur non trouvé dans la réponse${NC}" | tee -a $LOG_FILE
  echo "Réponse: $USER_RESPONSE" >> $LOG_FILE
  USER_ID="user-id-not-found"
else
  echo -e "${GREEN}Utilisateur créé avec succès. ID: ${YELLOW}$USER_ID${NC}" | tee -a $LOG_FILE
fi

echo "" | tee -a $LOG_FILE
echo -e "${GREEN}Connexion pour obtenir un jeton JWT...${NC}" | tee -a $LOG_FILE
AUTH_RESPONSE=$(curl -s -X POST $API_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "securepassword"
  }')

echo "$AUTH_RESPONSE" >> $LOG_FILE
TOKEN=$(echo "$AUTH_RESPONSE" | grep -o '"token":"[^"]*' | sed 's/"token":"//')

if [ -z "$TOKEN" ]; then
  echo -e "${RED}ERREUR: Token JWT non trouvé dans la réponse${NC}" | tee -a $LOG_FILE
  echo "Réponse: $AUTH_RESPONSE" >> $LOG_FILE
  TOKEN="jwt-token-not-found"
else
  echo -e "${GREEN}Connexion réussie. JWT obtenu.${NC}" | tee -a $LOG_FILE
fi

# ---------------------------------------------
# 2. TEST DES RELATIONS USER-PLACE
# ---------------------------------------------
echo "" | tee -a $LOG_FILE
echo -e "${BLUE}=== 2. TEST DES RELATIONS USER-PLACE ===${NC}" | tee -a $LOG_FILE

echo -e "${GREEN}Création d'un premier lieu...${NC}" | tee -a $LOG_FILE
PLACE1_RESPONSE=$(curl -s -X POST $API_URL/places \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Mountain Cabin",
    "description": "Cozy cabin in the mountains",
    "price": 120.50,
    "latitude": 40.7128,
    "longitude": -74.0060,
    "owner_id": "'"$USER_ID"'"
  }')

echo "$PLACE1_RESPONSE" >> $LOG_FILE
PLACE1_ID=$(echo "$PLACE1_RESPONSE" | grep -o '"id":"[^"]*' | sed 's/"id":"//')

if [ -z "$PLACE1_ID" ]; then
  echo -e "${RED}ERREUR: ID du premier lieu non trouvé dans la réponse${NC}" | tee -a $LOG_FILE
  echo "Réponse: $PLACE1_RESPONSE" >> $LOG_FILE
  PLACE1_ID="place1-id-not-found"
else
  echo -e "${GREEN}Premier lieu créé avec succès. ID: ${YELLOW}$PLACE1_ID${NC}" | tee -a $LOG_FILE
fi

echo "" | tee -a $LOG_FILE
echo -e "${GREEN}Création d'un second lieu...${NC}" | tee -a $LOG_FILE
PLACE2_RESPONSE=$(curl -s -X POST $API_URL/places \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Beach House",
    "description": "Beautiful house by the beach",
    "price": 200.00,
    "latitude": 25.7617,
    "longitude": -80.1918,
    "owner_id": "'"$USER_ID"'"
  }')

echo "$PLACE2_RESPONSE" >> $LOG_FILE
PLACE2_ID=$(echo "$PLACE2_RESPONSE" | grep -o '"id":"[^"]*' | sed 's/"id":"//')

if [ -z "$PLACE2_ID" ]; then
  echo -e "${RED}ERREUR: ID du second lieu non trouvé dans la réponse${NC}" | tee -a $LOG_FILE
  echo "Réponse: $PLACE2_RESPONSE" >> $LOG_FILE
  PLACE2_ID="place2-id-not-found"
else
  echo -e "${GREEN}Second lieu créé avec succès. ID: ${YELLOW}$PLACE2_ID${NC}" | tee -a $LOG_FILE
fi

echo "" | tee -a $LOG_FILE
echo -e "${GREEN}Récupération des lieux de l'utilisateur...${NC}" | tee -a $LOG_FILE
USER_PLACES_RESPONSE=$(curl -s -X GET "$API_URL/users/$USER_ID/places" \
  -H "Authorization: Bearer $TOKEN")

echo "$USER_PLACES_RESPONSE" >> $LOG_FILE
PLACES_COUNT=$(echo "$USER_PLACES_RESPONSE" | grep -o '"id"' | wc -l)

echo -e "${GREEN}L'utilisateur possède ${YELLOW}$PLACES_COUNT${GREEN} lieux.${NC}" | tee -a $LOG_FILE
echo -e "Vérification relation User-Place: ${YELLOW}$([ "$PLACES_COUNT" -eq 2 ] && echo "OK" || echo "ÉCHEC")${NC}" | tee -a $LOG_FILE

# ---------------------------------------------
# 3. TEST DES RELATIONS PLACE-REVIEW ET USER-REVIEW
# ---------------------------------------------
echo "" | tee -a $LOG_FILE
echo -e "${BLUE}=== 3. TEST DES RELATIONS PLACE-REVIEW ET USER-REVIEW ===${NC}" | tee -a $LOG_FILE

echo -e "${GREEN}Création d'un premier avis...${NC}" | tee -a $LOG_FILE
REVIEW1_RESPONSE=$(curl -s -X POST $API_URL/reviews \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "text": "Great place with amazing views!",
    "rating": 5,
    "place_id": "'"$PLACE1_ID"'",
    "user_id": "'"$USER_ID"'"
  }')

echo "$REVIEW1_RESPONSE" >> $LOG_FILE
REVIEW1_ID=$(echo "$REVIEW1_RESPONSE" | grep -o '"id":"[^"]*' | sed 's/"id":"//')

if [ -z "$REVIEW1_ID" ]; then
  echo -e "${RED}ERREUR: ID du premier avis non trouvé dans la réponse${NC}" | tee -a $LOG_FILE
  echo "Réponse: $REVIEW1_RESPONSE" >> $LOG_FILE
  REVIEW1_ID="review1-id-not-found"
else
  echo -e "${GREEN}Premier avis créé avec succès. ID: ${YELLOW}$REVIEW1_ID${NC}" | tee -a $LOG_FILE
fi

echo "" | tee -a $LOG_FILE
echo -e "${GREEN}Création d'un second avis...${NC}" | tee -a $LOG_FILE
REVIEW2_RESPONSE=$(curl -s -X POST $API_URL/reviews \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "text": "Comfortable and clean accommodation",
    "rating": 4,
    "place_id": "'"$PLACE1_ID"'",
    "user_id": "'"$USER_ID"'"
  }')

echo "$REVIEW2_RESPONSE" >> $LOG_FILE
REVIEW2_ID=$(echo "$REVIEW2_RESPONSE" | grep -o '"id":"[^"]*' | sed 's/"id":"//')

if [ -z "$REVIEW2_ID" ]; then
  echo -e "${RED}ERREUR: ID du second avis non trouvé dans la réponse${NC}" | tee -a $LOG_FILE
  echo "Réponse: $REVIEW2_RESPONSE" >> $LOG_FILE
  REVIEW2_ID="review2-id-not-found"
else
  echo -e "${GREEN}Second avis créé avec succès. ID: ${YELLOW}$REVIEW2_ID${NC}" | tee -a $LOG_FILE
fi

echo "" | tee -a $LOG_FILE
echo -e "${GREEN}Récupération des avis du lieu...${NC}" | tee -a $LOG_FILE
PLACE_REVIEWS_RESPONSE=$(curl -s -X GET "$API_URL/places/$PLACE1_ID/reviews" \
  -H "Authorization: Bearer $TOKEN")

echo "$PLACE_REVIEWS_RESPONSE" >> $LOG_FILE
PLACE_REVIEWS_COUNT=$(echo "$PLACE_REVIEWS_RESPONSE" | grep -o '"id"' | wc -l)

echo -e "${GREEN}Le lieu possède ${YELLOW}$PLACE_REVIEWS_COUNT${GREEN} avis.${NC}" | tee -a $LOG_FILE
echo -e "Vérification relation Place-Review: ${YELLOW}$([ "$PLACE_REVIEWS_COUNT" -eq 2 ] && echo "OK" || echo "ÉCHEC")${NC}" | tee -a $LOG_FILE

echo "" | tee -a $LOG_FILE
echo -e "${GREEN}Récupération des avis de l'utilisateur...${NC}" | tee -a $LOG_FILE
USER_REVIEWS_RESPONSE=$(curl -s -X GET "$API_URL/users/$USER_ID/reviews" \
  -H "Authorization: Bearer $TOKEN")

echo "$USER_REVIEWS_RESPONSE" >> $LOG_FILE
USER_REVIEWS_COUNT=$(echo "$USER_REVIEWS_RESPONSE" | grep -o '"id"' | wc -l)

echo -e "${GREEN}L'utilisateur a écrit ${YELLOW}$USER_REVIEWS_COUNT${GREEN} avis.${NC}" | tee -a $LOG_FILE
echo -e "Vérification relation User-Review: ${YELLOW}$([ "$USER_REVIEWS_COUNT" -eq 2 ] && echo "OK" || echo "ÉCHEC")${NC}" | tee -a $LOG_FILE

# ---------------------------------------------
# 4. TEST DES RELATIONS PLACE-AMENITY
# ---------------------------------------------
echo "" | tee -a $LOG_FILE
echo -e "${BLUE}=== 4. TEST DES RELATIONS PLACE-AMENITY ===${NC}" | tee -a $LOG_FILE

echo -e "${GREEN}Création d'un premier équipement...${NC}" | tee -a $LOG_FILE
AMENITY1_RESPONSE=$(curl -s -X POST $API_URL/amenities \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "WiFi"
  }')

echo "$AMENITY1_RESPONSE" >> $LOG_FILE
AMENITY1_ID=$(echo "$AMENITY1_RESPONSE" | grep -o '"id":"[^"]*' | sed 's/"id":"//')

if [ -z "$AMENITY1_ID" ]; then
  echo -e "${RED}ERREUR: ID du premier équipement non trouvé dans la réponse${NC}" | tee -a $LOG_FILE
  echo "Réponse: $AMENITY1_RESPONSE" >> $LOG_FILE
  AMENITY1_ID="amenity1-id-not-found"
else
  echo -e "${GREEN}Premier équipement créé avec succès. ID: ${YELLOW}$AMENITY1_ID${NC}" | tee -a $LOG_FILE
fi

echo "" | tee -a $LOG_FILE
echo -e "${GREEN}Création d'un second équipement...${NC}" | tee -a $LOG_FILE
AMENITY2_RESPONSE=$(curl -s -X POST $API_URL/amenities \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Swimming Pool"
  }')

echo "$AMENITY2_RESPONSE" >> $LOG_FILE
AMENITY2_ID=$(echo "$AMENITY2_RESPONSE" | grep -o '"id":"[^"]*' | sed 's/"id":"//')

if [ -z "$AMENITY2_ID" ]; then
  echo -e "${RED}ERREUR: ID du second équipement non trouvé dans la réponse${NC}" | tee -a $LOG_FILE
  echo "Réponse: $AMENITY2_RESPONSE" >> $LOG_FILE
  AMENITY2_ID="amenity2-id-not-found"
else
  echo -e "${GREEN}Second équipement créé avec succès. ID: ${YELLOW}$AMENITY2_ID${NC}" | tee -a $LOG_FILE
fi

echo "" | tee -a $LOG_FILE
echo -e "${GREEN}Association du premier équipement au lieu...${NC}" | tee -a $LOG_FILE
LINK1_RESPONSE=$(curl -s -X PUT "$API_URL/places/$PLACE1_ID/amenities/$AMENITY1_ID" \
  -H "Authorization: Bearer $TOKEN")
echo "$LINK1_RESPONSE" >> $LOG_FILE

echo -e "${GREEN}Association du second équipement au lieu...${NC}" | tee -a $LOG_FILE
LINK2_RESPONSE=$(curl -s -X PUT "$API_URL/places/$PLACE1_ID/amenities/$AMENITY2_ID" \
  -H "Authorization: Bearer $TOKEN")
echo "$LINK2_RESPONSE" >> $LOG_FILE

echo "" | tee -a $LOG_FILE
echo -e "${GREEN}Récupération des équipements du lieu...${NC}" | tee -a $LOG_FILE
PLACE_AMENITIES_RESPONSE=$(curl -s -X GET "$API_URL/places/$PLACE1_ID/amenities" \
  -H "Authorization: Bearer $TOKEN")

echo "$PLACE_AMENITIES_RESPONSE" >> $LOG_FILE
PLACE_AMENITIES_COUNT=$(echo "$PLACE_AMENITIES_RESPONSE" | grep -o '"id"' | wc -l)

echo -e "${GREEN}Le lieu possède ${YELLOW}$PLACE_AMENITIES_COUNT${GREEN} équipements.${NC}" | tee -a $LOG_FILE
echo -e "Vérification relation Place-Amenity: ${YELLOW}$([ "$PLACE_AMENITIES_COUNT" -eq 2 ] && echo "OK" || echo "ÉCHEC")${NC}" | tee -a $LOG_FILE

echo "" | tee -a $LOG_FILE
echo -e "${GREEN}Récupération des lieux avec le premier équipement...${NC}" | tee -a $LOG_FILE
AMENITY_PLACES_RESPONSE=$(curl -s -X GET "$API_URL/amenities/$AMENITY1_ID/places" \
  -H "Authorization: Bearer $TOKEN")

echo "$AMENITY_PLACES_RESPONSE" >> $LOG_FILE
AMENITY_PLACES_COUNT=$(echo "$AMENITY_PLACES_RESPONSE" | grep -o '"id"' | wc -l)

echo -e "${GREEN}L'équipement est présent dans ${YELLOW}$AMENITY_PLACES_COUNT${GREEN} lieux.${NC}" | tee -a $LOG_FILE
echo -e "Vérification relation Amenity-Place: ${YELLOW}$([ "$AMENITY_PLACES_COUNT" -ge 1 ] && echo "OK" || echo "ÉCHEC")${NC}" | tee -a $LOG_FILE

# ---------------------------------------------
# 5. TEST DU CHARGEMENT COMPLET D'UN LIEU AVEC DÉTAILS
# ---------------------------------------------
echo "" | tee -a $LOG_FILE
echo -e "${BLUE}=== 5. TEST DU CHARGEMENT COMPLET D'UN LIEU AVEC DÉTAILS ===${NC}" | tee -a $LOG_FILE

echo -e "${GREEN}Récupération des détails complets du lieu...${NC}" | tee -a $LOG_FILE
PLACE_DETAILS_RESPONSE=$(curl -s -X GET "$API_URL/places/$PLACE1_ID" \
  -H "Authorization: Bearer $TOKEN")

echo "$PLACE_DETAILS_RESPONSE" >> $LOG_FILE
HAS_OWNER=$(echo "$PLACE_DETAILS_RESPONSE" | grep -o '"user_id"' | wc -l)
HAS_REVIEWS=$(echo "$PLACE_DETAILS_RESPONSE" | grep -o '"reviews"' | wc -l)
HAS_AMENITIES=$(echo "$PLACE_DETAILS_RESPONSE" | grep -o '"amenities"' | wc -l)

echo -e "${GREEN}Vérification des détails du lieu:${NC}" | tee -a $LOG_FILE
echo -e "  - Information propriétaire: ${YELLOW}$([ "$HAS_OWNER" -eq 1 ] && echo "OK" || echo "ÉCHEC")${NC}" | tee -a $LOG_FILE
echo -e "  - Information avis: ${YELLOW}$([ "$HAS_REVIEWS" -eq 1 ] && echo "OK" || echo "ÉCHEC")${NC}" | tee -a $LOG_FILE
echo -e "  - Information équipements: ${YELLOW}$([ "$HAS_AMENITIES" -eq 1 ] && echo "OK" || echo "ÉCHEC")${NC}" | tee -a $LOG_FILE

# ---------------------------------------------
# RÉSUMÉ DES TESTS
# ---------------------------------------------
echo "" | tee -a $LOG_FILE
echo -e "${BLUE}=== RÉSUMÉ DES TESTS DE RELATIONS ===${NC}" | tee -a $LOG_FILE
echo -e "${GREEN}1. Relation User-Place: ${YELLOW}$([ "$PLACES_COUNT" -eq 2 ] && echo "OK" || echo "ÉCHEC")${NC}" | tee -a $LOG_FILE
echo -e "${GREEN}2. Relation Place-Review: ${YELLOW}$([ "$PLACE_REVIEWS_COUNT" -eq 2 ] && echo "OK" || echo "ÉCHEC")${NC}" | tee -a $LOG_FILE
echo -e "${GREEN}3. Relation User-Review: ${YELLOW}$([ "$USER_REVIEWS_COUNT" -eq 2 ] && echo "OK" || echo "ÉCHEC")${NC}" | tee -a $LOG_FILE
echo -e "${GREEN}4. Relation Place-Amenity: ${YELLOW}$([ "$PLACE_AMENITIES_COUNT" -eq 2 ] && echo "OK" || echo "ÉCHEC")${NC}" | tee -a $LOG_FILE

echo "" | tee -a $LOG_FILE
echo -e "${BLUE}Tests terminés. Résultats détaillés disponibles dans ${YELLOW}$LOG_FILE${NC}" | tee -a $LOG_FILE