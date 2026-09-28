FROM python:3.13.14-alpine3.24

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Patch OS packages, then create a user to run as instead of root.
RUN apk upgrade --no-cache && \
    adduser -D -u 10001 appuser

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy only what the app needs at runtime, so tests stay out of the image.
COPY app.py .
COPY templates/ ./templates/
COPY static/ ./static/

USER appuser

EXPOSE 5000

HEALTHCHECK --interval=15s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health').read()" || exit 1

# Gunicorn instead of the Flask development server, which is single-threaded
# and not built to face the internet.
#
# One worker with four threads: prometheus_client keeps its counters in process
# memory, so several workers would each hold a different partial count and
# Prometheus would scrape whichever one it happened to reach.
CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "1", \
     "--threads", "4", \
     "--access-logfile", "-", \
     "app:app"]
