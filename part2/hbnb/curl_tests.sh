#!/bin/bash

# API Tests and Documentation
# This script provides a set of curl commands to test the API endpoints
# and generates a Markdown report of the test results.

# Set the base URL for the API
BASE_URL="http://localhost:5000/api/v1"

# Initialize variables for test results
TOTAL_TESTS=0
PASSED_TESTS=0

# Initialize Markdown report
REPORT="# API Test Report\n\n"

# Function to run a test and update the report
run_test() {
    local description="$1"
    local command="$2"
    local expected_status="$3"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    echo "Running test: $description"
    
    # Run the curl command and capture the output and status code
    output=$(eval "$command -w \"\nStatus: %{http_code}\"")
    status=$(echo "$output" | sed -n '$p' | cut -d' ' -f2)
    body=$(echo "$output" | sed '$d')

    # Check if the status matches the expected status
    if [ "$status" -eq "$expected_status" ]; then
        echo "Test passed"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        result="✅ Passed"
    else
        echo "Test failed"
        result="❌ Failed"
    fi

    # Add test result to the report
    REPORT+="## Test: $description\n\n"
    REPORT+="**Result:** $result\n\n"
    REPORT+="**Expected Status:** $expected_status\n\n"
    REPORT+="**Actual Status:** $status\n\n"
    REPORT+="**Command:**\n\`\`\`bash\n$command\n\`\`\`\n\n"
    REPORT+="**Output:**\n\`\`\`json\n$body\n\`\`\`\n\n"
    REPORT+="---\n\n"
}

# User API Tests
run_test "Create a new user" "curl -s -X POST \"${BASE_URL}/users/\" -H \"Content-Type: application/json\" -d '{\"first_name\": \"John\", \"last_name\": \"Doe\", \"email\": \"john.doe@example.com\"}'" 201
USER_ID=$(echo "$body" | grep -o '"id":"[^"]*' | grep -o '[^"]*$')

run_test "Create a user with existing email" "curl -s -X POST \"${BASE_URL}/users/\" -H \"Content-Type: application/json\" -d '{\"first_name\": \"Jane\", \"last_name\": \"Doe\", \"email\": \"john.doe@example.com\"}'" 409

run_test "Get all users" "curl -s -X GET \"${BASE_URL}/users/\"" 200

run_test "Get a specific user" "curl -s -X GET \"${BASE_URL}/users/$USER_ID\"" 200

run_test "Update a user" "curl -s -X PUT \"${BASE_URL}/users/$USER_ID\" -H \"Content-Type: application/json\" -d '{\"first_name\": \"John\", \"last_name\": \"Smith\", \"email\": \"john.smith@example.com\"}'" 200

# Place API Tests
run_test "Create a new place" "curl -s -X POST \"${BASE_URL}/places/\" -H \"Content-Type: application/json\" -d '{\"name\": \"Cozy Apartment\", \"description\": \"A lovely place to stay\", \"number_rooms\": 2, \"number_bathrooms\": 1, \"max_guest\": 4, \"price_by_night\": 100, \"latitude\": 40.7128, \"longitude\": -74.0060, \"user_id\": \"$USER_ID\"}'" 201
PLACE_ID=$(echo "$body" | grep -o '"id":"[^"]*' | grep -o '[^"]*$')

run_test "Get all places" "curl -s -X GET \"${BASE_URL}/places/\"" 200

run_test "Get a specific place" "curl -s -X GET \"${BASE_URL}/places/$PLACE_ID\"" 200

run_test "Update a place" "curl -s -X PUT \"${BASE_URL}/places/$PLACE_ID\" -H \"Content-Type: application/json\" -d '{\"name\": \"Luxurious Apartment\", \"price_by_night\": 150}'" 200

# Amenity API Tests
run_test "Create a new amenity" "curl -s -X POST \"${BASE_URL}/amenities/\" -H \"Content-Type: application/json\" -d '{\"name\": \"Wi-Fi\"}'" 201
AMENITY_ID=$(echo "$body" | grep -o '"id":"[^"]*' | grep -o '[^"]*$')

run_test "Get all amenities" "curl -s -X GET \"${BASE_URL}/amenities/\"" 200

run_test "Get a specific amenity" "curl -s -X GET \"${BASE_URL}/amenities/$AMENITY_ID\"" 200

run_test "Update an amenity" "curl -s -X PUT \"${BASE_URL}/amenities/$AMENITY_ID\" -H \"Content-Type: application/json\" -d '{\"name\": \"High-speed Wi-Fi\"}'" 200

# Review API Tests
run_test "Create a new review" "curl -s -X POST \"${BASE_URL}/reviews/\" -H \"Content-Type: application/json\" -d '{\"text\": \"Great place to stay!\", \"rating\": 5, \"user_id\": \"$USER_ID\", \"place_id\": \"$PLACE_ID\"}'" 201
REVIEW_ID=$(echo "$body" | grep -o '"id":"[^"]*' | grep -o '[^"]*$')

run_test "Get all reviews" "curl -s -X GET \"${BASE_URL}/reviews/\"" 200

run_test "Get a specific review" "curl -s -X GET \"${BASE_URL}/reviews/$REVIEW_ID\"" 200

run_test "Update a review" "curl -s -X PUT \"${BASE_URL}/reviews/$REVIEW_ID\" -H \"Content-Type: application/json\" -d '{\"text\": \"Amazing place, highly recommended!\", \"rating\": 5}'" 200

# Generate test summary
REPORT+="# Test Summary\n\n"
REPORT+="Total tests: $TOTAL_TESTS\n"
REPORT+="Passed tests: $PASSED_TESTS\n"
REPORT+="Failed tests: $((TOTAL_TESTS - PASSED_TESTS))\n"

# Save the report to a Markdown file
echo -e "$REPORT" > api_test_report.md

echo "API Testing Complete. Report saved to api_test_report.md"
