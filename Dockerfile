FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN python -m pip install --no-deps .

RUN useradd --create-home --uid 10001 ghostledger
USER ghostledger
ENTRYPOINT ["ghostledger"]
CMD ["doctor"]
