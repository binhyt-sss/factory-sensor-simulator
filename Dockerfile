FROM python:3.10-slim

WORKDIR /app

COPY . /app

# Tạo virtual environment
RUN python -m venv .venv \
    && .venv/bin/pip install --upgrade pip \
    && .venv/bin/pip install --no-cache-dir -r requirements.txt

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app

ENTRYPOINT ["/app/.venv/bin/python", "src/thingsboard/main.py"] 