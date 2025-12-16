# Dockerfile (Backend)
FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ENV PYTHONPATH=/app/src

COPY pyproject.toml /app/

# Copier le code source
COPY src/ /app/src


# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    fastapi \
    pydantic \
    uvicorn


EXPOSE 8000

# Commande de démarrage (le chemin d'accès reste le même)
CMD ["uvicorn", "src.cicd.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]