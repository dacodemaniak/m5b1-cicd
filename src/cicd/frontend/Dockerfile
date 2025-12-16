FROM python:3.11-slim


ENV PYTHONUNBUFFERED 1


WORKDIR /app


COPY pyproject.toml poetry.lock ./


RUN pip install poetry


RUN poetry install --no-root --only main


COPY frontend/app.py /app/

ENV API_BASE_URL http://backend:8000


EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]