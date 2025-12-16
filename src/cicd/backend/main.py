from fastapi import FastAPI
from pydantic import BaseModel
from cicd.backend.modules.calcul import square

# Init FastAPI application
app = FastAPI(
    title="Square calculator API",
    description="Simple API using Pydantic to validate a square calcul"
)

# Sets Pydantic scheme for POST entry
class SquareInput(BaseModel):
    number: int # Ensure an int was passed

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "number": 7
                }
            ]
        }
    }

# API Endpoints
@app.get("/", tags=["Basic"])
def home():
    return {"message": "Welcome to simple square API"}

@app.get("/health", tags=["Basic"])
def health_check():
    return {"status": "ok", "service": "square-calculator"}

@app.post("/square", tags=["Calcul"])
def post_square(data: SquareInput):
    input_number = data.number # Pydantic validation

    result = square(input_number)

    return {"square": result}