#!/bin/bash
# ========================================
# Demo Script for Hypertension Adherence API
# ========================================

BASE_URL="http://127.0.0.1:8000/api"
USERNAME="demo_user"
EMAIL="demo@example.com"
PASSWORD="DemoPass123"

echo "1) Register a new user..."
curl -s -X POST $BASE_URL/auth/register/ \
-H "Content-Type: application/json" \
-d "{\"username\": \"$USERNAME\", \"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}"
echo -e "\n"

echo "2) Login to get JWT token..."
TOKEN=$(curl -s -X POST $BASE_URL/auth/login/ \
-H "Content-Type: application/json" \
-d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}" -r '.access')

echo "Token received: $TOKEN"
echo -e "\n"

echo "3) Get medication list (empty initially)..."
curl -s -X GET $BASE_URL/medications/ \
-H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "4) Add a medication..."
curl -s -X POST $BASE_URL/medications/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
-d '{"name": "Amlodipine", "dosage": "5mg", "schedule": "Once daily"}'
echo -e "\n"

echo "5) Log medication adherence..."
curl -s -X POST $BASE_URL/adherence/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
-d '{"medication_id": 1, "taken": true, "timestamp": "2025-08-26T08:00:00Z"}'
echo -e "\n"

echo "6) Try accessing medications WITHOUT token (should fail)..."
curl -s -X GET $BASE_URL/medications/
echo -e "\n"

echo "✅ Demo complete!"
