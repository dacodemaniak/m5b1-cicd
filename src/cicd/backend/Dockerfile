# Light Python image
FROM python:3.11-slim

# No buffer input / output setting
ENV PYTHONUNBUFFERED 1

# Container workdir
WORKDIR /app

# Copy files from dependencies
# Docker cache is used if no changes
COPY pyproject.toml poetry.lock ./

# Poetry installation
RUN pip install poetry

# Install only production dependencies
# --no-root no package for app
RUN poetry install --no-root --only main


COPY backend /app/backend

# Expose API port
EXPOSE 8000

# Backend bootstrap
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]