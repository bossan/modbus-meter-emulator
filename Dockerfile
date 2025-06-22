FROM python:3.13-slim AS builder

RUN pip install poetry==2.1.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

FROM python:3.13-slim AS final

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY modbus_meter_emulator ./modbus_meter_emulator
COPY config.example.yaml /etc/modbus-meter/config.yaml

ENTRYPOINT ["python", "-m", "modbus_meter_emulator", "/etc/modbus-meter/config.yaml"]
