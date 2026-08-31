FROM ghcr.io/astral-sh/uv:python3.14-alpine AS builder

WORKDIR /build
COPY . .

RUN uv build --wheel

FROM ghcr.io/astral-sh/uv:python3.14-alpine

WORKDIR /app
COPY --from=builder /build/dist/*.whl ./

ENV UV_SYSTEM_PYTHON=1
RUN uv pip install *.whl && rm *.whl

ENV CONFIG_DIR=/config
ENV DATA_DIR=/data

COPY entrypoint.sh .
COPY alembic.ini .
COPY migrations/ ./migrations

ENTRYPOINT ["./entrypoint.sh"]

CMD ["python", "-m", "app"]
