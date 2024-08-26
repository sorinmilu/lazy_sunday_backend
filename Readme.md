uvicorn app.main:app --reload

1. fill out the .env

for local:

STORAGE_MODE=localfile
DB_HOST=localhost
DB_USERNAME=user
DB_PASSWORD=secret
DB_NAME=your_database_name

for keyvault: 

.env or environment variables: 
STORAGE_MODE=azurekeyvault
KEY_VAULT_NAME=your-key-vault-name
DB_HOST_SECRET_NAME=host-secret-name
DB_USERNAME_SECRET_NAME=username-secret-name
DB_PASSWORD_SECRET_NAME=password-secret-name
DB_NAME_SECRET_NAME=db-name-secret-name


2. run the alembic first time

`alembic revision --autogenerate -m "Initial migration"`
`alembic upgrade head`

`python populatedb.py populate`


3. when you generate a new migration (changes in models) you do this: 
`alembic revision --autogenerate -m "Describe your changes"`
`alembic upgrade head`

other alembic util commands:

`alembic history - list migration history`
`alembic current - show curent migration`
`alembic show <revision_id> - shows revision id`


Reseting the database is manual - drop the scheme, recreate, delete all version files from alembic/versions/*.py

Keep alembic outside of git for now, we do not use continuous deployment so every time the app is deployed the last version will be installed. 

## Running

uvicorn app.main:app --reload

## Using



curl -X POST "http://localhost:8000/token" -H "Content-Type: application/x-www-form-urlencoded" -d "username=sorin&password=larevedere"

curl -X POST "http://localhost:8000/users/" -H "Content-Type: application/json" -d '{"username":"sorin", "password":"larevedere"}'

curl -X GET "http://localhost:8000/tasks/" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzb3JpbiIsImV4cCI6MTcyNDU5ODM1NH0.V7JrwyiLvIq9k07ujFy4taZL5fpWEXH4yi73raoWQMQ"

