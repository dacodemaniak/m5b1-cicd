# frontend/Dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app


COPY pyproject.toml /app/
# Copier le code Streamlit et les modules nécessaires
COPY src/cicd/frontend/app.py /app/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    streamlit \
    loguru \
    requests


ENV API_BASE_URL http://backend:8000

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]