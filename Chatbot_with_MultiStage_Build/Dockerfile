FROM python:3.10-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
    --prefix=/install \
    -r requirements.txt

COPY . .

# Runtime stage
FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /install /usr/local
COPY --from=builder /app .

EXPOSE 5000

CMD ["python","app.py"]
