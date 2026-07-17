FROM ghcr.io/astral-sh/uv:0.11.29-python3.14-trixie-slim

WORKDIR /src

COPY . /src

ENV UV_NO_DEV=1

RUN uv sync --locked

EXPOSE 8000

CMD ["python -m src.main"]