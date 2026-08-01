from datetime import datetime, timezone

import psutil
from flask import Flask, jsonify, render_template
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

app = Flask(__name__)

APP_VERSION = "1.0.0"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify(
        service="system-status-dashboard",
        status="healthy",
        version=APP_VERSION
    )


@app.route("/metrics-data")
def metrics_data():
    boot_time = datetime.fromtimestamp(
        psutil.boot_time(),
        tz=timezone.utc
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
        version=APP_VERSION
    )


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)