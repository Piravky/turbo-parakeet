FROM python:3.12-slim AS builder

USER root

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY pyproject.toml poetry.lock ./

RUN pip install poetry

ENV PATH="/root/.local/bin:$PATH"

RUN poetry install --no-root --no-cache

FROM python:3.12-slim AS runtime

WORKDIR /app

USER root

RUN pip install poetry

COPY --from=builder /root/.cache/pypoetry/virtualenvs /root/.cache/pypoetry/virtualenvs
COPY --from=builder /app/pyproject.toml /app/poetry.lock ./

COPY src/ ./src/
COPY migration/ ./migration/
COPY alembic.ini .
COPY .env .

ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH="${PYTHONPATH}:/app/src"

EXPOSE 8000


CMD ["sh", "-c", "poetry run alembic upgrade head && poetry run python3 src/main.py"]
