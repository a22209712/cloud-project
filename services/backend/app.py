from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Backend Running"

@app.route("/api/status")
def status():
    return {
        "status": "running",
        "service": "backend"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)