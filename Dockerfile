# Dockerfile

FROM python:3.10

ENV PYTHONPATH=/app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY quiz.db ./quiz.db

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

