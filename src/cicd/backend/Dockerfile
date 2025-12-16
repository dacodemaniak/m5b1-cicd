# Dockerfile (Backend)
FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app


COPY pyproject.toml /app/
# NOTE: Nous n'avons pas besoin de setup.cfg ou requirements.txt avec cette approche

# Copier le code source
COPY src/cicd/backend /app/src

RUN pip install --no-cache-dir .


EXPOSE 8000

# Commande de démarrage (le chemin d'accès reste le même)
CMD ["uvicorn", "src.cicd.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]