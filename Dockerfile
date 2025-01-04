# Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m myuser
RUN chown -R myuser:myuser /app
# Add permissions for volume directories
RUN mkdir -p /app/db /app/media && \
    chown -R myuser:myuser /app/db /app/media && \
    chmod -R 755 /app/db /app/media
USER myuser

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]