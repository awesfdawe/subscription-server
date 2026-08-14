FROM ghcr.io/astral-sh/uv:python3.14-alpine AS builder

WORKDIR /build
COPY . .

RUN uv build --wheel

FROM ghcr.io/astral-sh/uv:python3.14-alpine

VOLUME [ "/data", "/config" ]

WORKDIR /app
COPY --from=builder /build/dist/*.whl ./

ENV UV_SYSTEM_PYTHON=1
RUN uv pip install *.whl && rm *.whl

COPY entrypoint.sh .
COPY alembic.ini .
COPY migrations/ ./migrations
COPY config/xray_template.json /config/

ENTRYPOINT ["./entrypoint.sh"]

CMD ["python", "-m", "app"]
