from flask import Flask, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "demo_app_requests_total",
    "Total number of HTTP requests handled by demo-app.",
    ["path"],
)


@app.route("/")
def index():
    REQUEST_COUNT.labels(path="/").inc()
    return {
        "message": "prometheus-grafana-demo is running",
        "metrics": "/metrics",
    }


@app.route("/hello")
def hello():
    REQUEST_COUNT.labels(path="/hello").inc()
    return {"message": "hello from demo-app"}


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
