@app.route("/gerar", methods=["POST"])
def gerar():
    print("POST RECEBIDO")

    dados = request.json

    return jsonify({
        "status": "ok",
        "dados": dados
    })
