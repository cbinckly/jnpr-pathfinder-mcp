FROM ghcr.io/astral-sh/uv:bookworm-slim

WORKDIR /app

COPY . /app

RUN uv sync --locked

EXPOSE 8888

CMD ["uv", "run", "-m", "jnpr_pathfinder_mcp", "--transport", "http", "--host", "0.0.0.0", "--port", "8888"]
