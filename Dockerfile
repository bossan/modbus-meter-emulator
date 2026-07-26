FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY modbus_meter_emulator ./modbus_meter_emulator

RUN uv sync --locked --no-dev --no-editable

FROM python:3.14-slim AS final

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY config.example.yaml /etc/modbus-meter/config.yaml

ENTRYPOINT ["python", "-m", "modbus_meter_emulator", "/etc/modbus-meter/config.yaml"]
