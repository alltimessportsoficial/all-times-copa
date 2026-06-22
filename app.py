from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "All Times Sports - Copa 2026 API Online!"

@app.route("/gerar", methods=["POST"])
def gerar():
    dados = request.json
    print(dados)

    return jsonify({
        "dados": dados,
        "status": "ok"
    })

if __name__ == "__main__":
    app.run()
