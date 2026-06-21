from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "All Times Sports - Copa 2026 API Online!"
