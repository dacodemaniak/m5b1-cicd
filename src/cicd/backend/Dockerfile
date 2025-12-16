FROM python:3.11-slim

LABEL org.opencontainers.image.title="Square Calculator Backend"
LABEL org.opencontainers.image.description="FastAPI backend for square calculation"
LABEL org.opencontainers.image.version="0.1.0"
LABEL org.opencontainers.image.authors="Dacodemaniak"

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