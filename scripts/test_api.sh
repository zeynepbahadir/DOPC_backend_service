#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Starting API tests..."

# Base URL and common parameters
BASE_URL="http://localhost:8000/api/v1"
VENUE_SLUG="home-assignment-venue-berlin"


# Test 1: /api/v1/delivery-order-price GET request 
echo -e "\n${GREEN}Test 1: /api/v1/delivery-order-price GET request${NC}"
response=$(curl -s -w "%{http_code}" "${BASE_URL}/delivery-order-price?venue_slug=${VENUE_SLUG}&cart_value=2000&user_lat=41.9028&user_lon=12.4964" \
  -H 'Accept: application/json' \
  -H 'Cache-Control: max-age=0' \
  -H 'Connection: keep-alive')


status=$(echo "$response" | tail -n1)
if [ $status -eq 200 ]; then
    echo -e "${GREEN}✓ Status is 200${NC}" 
else
    echo -e "${RED}✗ Status is not 200${NC}" "$status"
fi
echo "response: $response"

echo -e "\n${GREEN}API tests completed!${NC}" 
