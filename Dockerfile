# ──────────────────────────────────────────────
# Stage 1 – Builder
# ──────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

# System deps required to compile psycopg2 and Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt

# ──────────────────────────────────────────────
# Stage 2 – Runtime
# ──────────────────────────────────────────────
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Runtime system libs only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libjpeg62-turbo \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy project source
COPY . .

# Collect static files (no DB needed at build time)
RUN python manage.py collectstatic --noinput || true

# Create a non-root user
RUN addgroup --system django && adduser --system --ingroup django django
USER django

EXPOSE 8000

# Entrypoint: run migrations then start Gunicorn
CMD ["sh", "-c", \
  "python manage.py migrate --noinput && \
   gunicorn anupam_bearings.wsgi:application \
     --bind 0.0.0.0:${PORT} \
     --workers 3 \
     --timeout 120"]