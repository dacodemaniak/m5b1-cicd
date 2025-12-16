# m5b1-cicd : Simple Python app illustrating CI/CD concepts

## Backend

Expose :

- GET / : simple text
- GET /health : simple health endpoint
- POST /square : Returns the square of an integer

Pydantic is used from BaseModel to ensure that an integer is passed to API.
If not, a 422 status is returned

**Unit testing**:
`poetry run pytest`

## Docker

`docker compose up -d`

**Test API**

`curl http://backend:8000/`

**Load frontend**
`http://localhost:8501`

## Webhook

URL (secret): CI/CD Bot on Discord Server
