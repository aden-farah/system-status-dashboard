from datetime import datetime, timezone
from time import perf_counter

import psutil
from flask import Flask, g, jsonify, render_template, request
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Histogram,
    generate_latest,
)

app = Flask(__name__)

APP_VERSION = "1.0.0"


# Counts HTTP requests by method, endpoint and status code.
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status_code"],
)

# Measures how long requests take.
HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)


@app.before_request
def start_request_timer():
    # Prometheus visits /metrics every 5 seconds.
    # We exclude it so it does not inflate the application traffic numbers.
    if request.endpoint != "metrics":
        g.request_start_time = perf_counter()


@app.after_request
def record_request_metrics(response):
    if request.endpoint != "metrics":
        endpoint = request.endpoint or "unknown"

        HTTP_REQUESTS_TOTAL.labels(
            method=request.method,
            endpoint=endpoint,
            status_code=response.status_code,
        ).inc()

        start_time = getattr(g, "request_start_time", None)

        if start_time is not None:
            duration = perf_counter() - start_time

            HTTP_REQUEST_DURATION_SECONDS.labels(
                method=request.method,
                endpoint=endpoint,
            ).observe(duration)

    return response


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify(
        service="system-status-dashboard",
        status="healthy",
        version=APP_VERSION,
    )


@app.route("/metrics-data")
def metrics_data():
    boot_time = datetime.fromtimestamp(
        psutil.boot_time(),
        tz=timezone.utc,
    )

    uptime_seconds = int(
        (datetime.now(timezone.utc) - boot_time).total_seconds()
    )

    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)

    if days > 0:
        uptime = f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        uptime = f"{hours}h {minutes}m"
    else:
        uptime = f"{minutes}m"

    return jsonify(
        cpu=round(psutil.cpu_percent(interval=0.2), 1),
        memory=round(psutil.virtual_memory().percent, 1),
        disk=round(psutil.disk_usage("/").percent, 1),
        uptime=uptime,
        version=APP_VERSION,
    )


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )