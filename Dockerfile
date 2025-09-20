FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV PORT=8080

EXPOSE 8080

# Use ddtrace-run with gunicorn for automatic tracing
CMD ["ddtrace-run", "gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--timeout", "30", "app:app"]