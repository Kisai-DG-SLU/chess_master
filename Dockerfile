FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y stockfish curl && rm -rf /var/lib/apt/lists/*

COPY pixi.toml .
COPY pyproject.toml .

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    pydantic \
    langchain-core \
    langgraph \
    langchain-openai \
    pymilvus \
    requests \
    stockfish \
    pytest

COPY agent/ ./agent/
COPY api/ ./api/
COPY rag/ ./rag/

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
