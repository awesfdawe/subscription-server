FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS builder

WORKDIR /build
COPY . .

RUN uv build --wheel

FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim

WORKDIR /app
COPY --from=builder /build/dist/*.whl ./

ENV UV_SYSTEM_PYTHON=1
RUN uv pip install *.whl && rm *.whl

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
COPY alembic.ini .
COPY migrations/ ./migrations

ENTRYPOINT ["./entrypoint.sh"]

CMD ["python", "-m", "app"]
