FROM python:3.11-slim

WORKDIR /app

# Instalación de ffmpeg y dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV PORT=8000

EXPOSE 8000

# Usar la variable de entorno $PORT asignada dinámicamente por Render (default: 8000)
CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"
