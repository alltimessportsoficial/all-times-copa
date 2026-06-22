from flask import Flask, request, jsonify
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


@app.route("/gerar", methods=["POST"])
def gerar():

    dados = request.json

    selecao1 = dados["selecao1"]
    selecao2 = dados["selecao2"]
    url1 = dados["url1"]
    url2 = dados["url2"]
    data = dados.get("data", "")
    hora = dados.get("hora", "")

    fundo = Image.open("assets/fundo.png").convert("RGBA")
    draw = ImageDraw.Draw(fundo)

    camisa1 = Image.open(
        BytesIO(requests.get(url1).content)
    ).convert("RGBA")

    camisa2 = Image.open(
        BytesIO(requests.get(url2).content)
    ).convert("RGBA")

    camisa1.thumbnail((500, 500))
    camisa2.thumbnail((500, 500))

    largura, altura = fundo.size

    x1 = largura // 2 - 450
    x2 = largura // 2 + 150
    y = altura // 2 - 100

    fundo.paste(camisa1, (x1, y), camisa1)
    fundo.paste(camisa2, (x2, y), camisa2)

    try:
        fonte_titulo = ImageFont.truetype(
            "assets/BebasNeue-Regular.ttf", 110
        )
        fonte_texto = ImageFont.truetype(
            "assets/Montserrat-Bold.ttf", 45
        )
    except:
        fonte_titulo = ImageFont.load_default()
        fonte_texto = ImageFont.load_default()

    titulo = f"{selecao1.upper()} X {selecao2.upper()}"

    bbox = draw.textbbox((0, 0), titulo, font=fonte_titulo)
    largura_texto = bbox[2] - bbox[0]

    draw.text(
        ((largura - largura_texto) / 2, 120),
        titulo,
        fill="white",
        font=fonte_titulo
    )

    subtitulo = f"{data} • {hora}"

    draw.text(
        (largura / 2 - 150, altura - 260),
        subtitulo,
        fill="gold",
        font=fonte_texto
    )

    draw.text(
        (largura / 2 - 350, altura - 180),
        "AS CAMISAS DA COPA VOCÊ ENCONTRA NA ATS",
        fill="white",
        font=fonte_texto
    )

    nome = (
        f"{selecao1}_{selecao2}_"
        f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    )

    caminho = f"output/{nome}"

    fundo.save(caminho)

    return jsonify({
        "arquivo": nome,
        "status": "ok"
    })


if __name__ == "__main__":
    app.run()
