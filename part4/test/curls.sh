# Get all users
curl -X 'GET' \
  'http://127.0.0.1:5000/api/v1/users/' \
  -H 'accept: application/json'

# Create user
curl -X 'POST' \
  'http://127.0.0.1:5000/api/v1/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "Fer",
  "last_name": "Fal",
  "email": "fer@fal.con",
  "password": "123456",
  "is_admin": false
}'

# Authenticate user
curl -X 'POST' \
  'http://127.0.0.1:5000/api/v1/auth/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "fer@fal.con",
  "password": "123456"
}'

# Create place
curl -X 'POST' \
  'http://127.0.0.1:5000/api/v1/places/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1MjM0NTg1MywianRpIjoiMjQ4YjZkZmItNDY1Ni00ODMxLWFjZDgtMjAzZmFkYjViNGFlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjA5MWMzMTdjLWViYTYtNDkxZi04MGQzLTM4YjhmNmMyNzk4MyIsIm5iZiI6MTc1MjM0NTg1MywiY3NyZiI6ImZmYWFjYWNiLWNhOTEtNDZkNS04NjljLTkyYzQ3ZmM3ZGQ0MiIsImV4cCI6MTc1MjM0Njc1M30.xdTsvmuu6kw8OqwpzVziX718cLqT9NLJ8Es4awJXhaU" \
  -d '{
  "title": "string",
  "description": "string",
  "price": 0,
  "latitude": 0,
  "longitude": 0,
  "amenity_ids": [
    "string"
  ]
}'