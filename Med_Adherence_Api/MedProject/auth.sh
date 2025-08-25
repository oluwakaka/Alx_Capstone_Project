#!/bin/bash
# ==============================
# Django SimpleJWT Auto Login Script (jq-free)
# ==============================

API_URL="http://127.0.0.1:8000"
USERNAME="kaka"                # change to your username
PASSWORD="yourpassword"        # change to your password

# Step 1: Login and get tokens
TOKENS=$(curl -s -X POST $API_URL/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}")

# Step 2: Extract tokens using Python (no jq needed)
ACCESS=$(python -c "import sys, json; print(json.loads(sys.argv[1]).get('access',''))" "$TOKENS")
REFRESH=$(python -c "import sys, json; print(json.loads(sys.argv[1]).get('refresh',''))" "$TOKENS")

if [ -z "$ACCESS" ] || [ "$ACCESS" = "null" ]; then
  echo "❌ Login failed. Check username/password."
  echo $TOKENS
  exit 1
fi

echo "✅ Logged in as $USERNAME"
echo "Access Token: $ACCESS"
echo "Refresh Token: $REFRESH"

# Step 3: Save tokens for later use
echo $ACCESS > .access_token
echo $REFRESH > .refresh_token
