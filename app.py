from flask import Flask, request, jsonify, send_from_directory
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os
from datetime import datetime

app = Flask(__name__)

os.makedirs("output", exist_ok=True)


@app.route("/")
def home():
    return "All Times Sports - Copa 2026 API Online!"


@app.route("/output/<nome>")
def baixar(nome):
    return send_from_directory("output", nome)


@app.route("/gerar", methods=["POST"])
def gerar():
    try:
        dados = request.get_json(force=True)

        selecao1 = dados["selecao1"]
        selecao2 = dados["selecao2"]
        url1 = dados["url1"]
        url2 = dados["url2"]
        data = dados.get("data", "")
        hora = dados.get("hora", "")

        # Fundo
        fundo = Image.open("assets/fundo.png").convert("RGBA")
        draw = ImageDraw.Draw(fundo)

        # Download das camisas
        resposta1 = requests.get(url1, timeout=20)
        resposta2 = requests.get(url2, timeout=20)

        resposta1.raise_for_status()
        resposta2.raise_for_status()

        camisa1 = Image.open(
            BytesIO(resposta1.content)
        ).convert("RGBA")

        camisa2 = Image.open(
            BytesIO(resposta2.content)
        ).convert("RGBA")

        camisa1.thumbnail((650, 650))
        camisa2.thumbnail((650, 650))

        largura, altura = fundo.size

        x1 = largura // 2 - 450
        x2 = largura // 2 + 150
        y = altura // 2 - 180

        fundo.paste(camisa1, (x1, y), camisa1)
        fundo.paste(camisa2, (x2, y), camisa2)

        # Fontes
        try:
            fonte_titulo = ImageFont.truetype(
                "assets/BebasNeue-Regular.ttf",
                110
            )

            fonte_texto = ImageFont.truetype(
                "assets/Montserrat-Bold.ttf",
                45
            )

        except:
            fonte_titulo = ImageFont.load_default()
            fonte_texto = ImageFont.load_default()

        # Título
        titulo = f"{selecao1.upper()} X {selecao2.upper()}"

        bbox = draw.textbbox(
            (0, 0),
            titulo,
            font=fonte_titulo
        )

        largura_texto = bbox[2] - bbox[0]

        draw.text(
            (
                (largura - largura_texto) / 2,
                120
            ),
            titulo,
            fill="white",
            font=fonte_titulo
        )

        # Data e hora
        subtitulo = f"{data} • {hora}"

        bbox2 = draw.textbbox(
            (0, 0),
            subtitulo,
            font=fonte_texto
        )

        largura2 = bbox2[2] - bbox2[0]

        draw.text(
            (
                (largura - largura2) / 2,
                altura - 260
            ),
            subtitulo,
            fill="gold",
            font=fonte_texto
        )

        # Rodapé
        rodape = "AS CAMISAS DA COPA VOCÊ ENCONTRA NA ATS"

        bbox3 = draw.textbbox(
            (0, 0),
            rodape,
            font=fonte_texto
        )

        largura3 = bbox3[2] - bbox3[0]

        draw.text(
            (
                (largura - largura3) / 2,
                altura - 180
            ),
            rodape,
            fill="white",
            font=fonte_texto
        )

        # Nome do arquivo
        nome = (
            f"{selecao1}_{selecao2}_"
            f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        )

        nome = nome.replace(" ", "_")

        caminho = f"output/{nome}"

        fundo.save(caminho)

        return jsonify({
            "status": "ok",
            "arquivo": nome,
            "url": request.host_url + "output/" + nome
        })

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
