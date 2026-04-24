FROM python:3.10-slim

WORKDIR /app

ENV PATH="/usr/games:${PATH}"

RUN apt-get -o APT::Sandbox::User=root update && \
    apt-get -o APT::Sandbox::User=root install -y stockfish curl && \
    rm -rf /var/lib/apt/lists/*

COPY pixi.toml .
COPY pyproject.toml .

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    pydantic \
    langchain-core \
    langgraph \
    langchain-openai \
    openai \
    pymilvus \
    requests \
    google-api-python-client \
    stockfish \
    pytest pymongo

COPY agent/ ./agent/
COPY api/ ./api/
COPY rag/ ./rag/

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
