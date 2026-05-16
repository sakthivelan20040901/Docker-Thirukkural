FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    -r requirements.txt

RUN python -c "import nltk; nltk.download('stopwords')"

EXPOSE 5000

CMD ["python", "app.py"]
