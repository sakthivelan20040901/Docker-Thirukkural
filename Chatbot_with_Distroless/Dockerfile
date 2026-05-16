FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM gcr.io/distroless/python3-debian12

WORKDIR /app

# Copy entire Python installation
COPY --from=builder /usr/local /usr/local

# Copy app
COPY --from=builder /app /app

ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages

EXPOSE 5000

CMD ["app.py"]
