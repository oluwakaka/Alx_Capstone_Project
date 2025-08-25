#!/bin/bash
# ==============================
# Call API with Saved Token (jq-free)
# ==============================

API_URL="http://127.0.0.1:8000"

if [ ! -f .access_token ]; then
  echo "❌ No access token found. Please run ./auth.sh first."
  exit 1
fi

ACCESS=$(cat .access_token)

# Example: create a schedule (you can change the payload)
curl -X POST $API_URL/api/schedules/ \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"patient":1,"medication_name":"Amlodipine","dosage":"5mg","frequency":"once daily","start_date":"2025-08-01","end_date":"2026-08-01"}'
