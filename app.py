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


@app.route("/imagem/<arquivo>")
def imagem(arquivo):
    return send_from_directory("output", arquivo)


@app.route("/gerar", methods=["POST"])
def gerar():

    dados = request.get_json()

    selecao1 = dados["selecao1"]
    selecao2 = dados["selecao2"]
    url1 = dados["url1"]
    url2 = dados["url2"]
    data = dados.get("data", "")
    hora = dados.get("hora", "")

    fundo = Image.open("assets/fundo.png").convert("RGBA")
    draw = ImageDraw.Draw(fundo)

    # BAIXA CAMISA 1
    r1 = requests.get(url1)

    if "image" not in r1.headers.get("Content-Type", ""):
        return jsonify({
            "status": "erro",
            "mensagem": f"URL1 não é uma imagem: {url1}"
        }), 400

    camisa1 = Image.open(
        BytesIO(r1.content)
    ).convert("RGBA")

    # BAIXA CAMISA 2
    r2 = requests.get(url2)

    if "image" not in r2.headers.get("Content-Type", ""):
        return jsonify({
            "status": "erro",
            "mensagem": f"URL2 não é uma imagem: {url2}"
        }), 400

    camisa2 = Image.open(
        BytesIO(r2.content)
    ).convert("RGBA")

    # TAMANHO DAS CAMISAS
    camisa1.thumbnail((600, 600))
    camisa2.thumbnail((600, 600))

    largura, altura = fundo.size

    x1 = largura // 2 - 620
    x2 = largura // 2 - 20
    y = altura // 2 - 180

    fundo.paste(camisa1, (x1, y), camisa1)
    fundo.paste(camisa2, (x2, y), camisa2)

    # FONTES
    print(os.listdir("assets"))
    try:
        fonte_titulo = ImageFont.truetype(
            "assets/BebasNeue-Regular.ttf",
            110
        )
    
        fonte_texto = ImageFont.truetype(
            "assets/Montserrat-VariableFont_wght.ttf",
            70
        )
    
        print("FONTES CARREGADAS")
    
    except Exception as e:
        print("ERRO NAS FONTES:", e)
    
        fonte_titulo = ImageFont.load_default()
        fonte_texto = ImageFont.load_default()

    # TÍTULO
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
            80
        ),
        titulo,
        fill="white",
        font=fonte_titulo
    )

    # DATA E HORA
    subtitulo = f"{data} • {hora}"

    bbox2 = draw.textbbox(
        (0, 0),
        subtitulo,
        font=fonte_texto
    )

    largura_sub = bbox2[2] - bbox2[0]

    draw.text(
        (
            (largura - largura_sub) / 2,
            altura - 300
        ),
        subtitulo,
        fill="gold",
        font=fonte_texto
    )

    # SLOGAN
    slogan = "AS CAMISAS DA COPA VOCÊ ENCONTRA NA ATS"

    bbox3 = draw.textbbox(
        (0, 0),
        slogan,
        font=fonte_texto
    )

    largura_slogan = bbox3[2] - bbox3[0]

    draw.text(
        (
            (largura - largura_slogan) / 3,
            altura - 200
        ),
        slogan,
        fill="white",
        font=fonte_texto
    )

    # SALVA ARQUIVO
    nome = (
        f"{selecao1}_{selecao2}_"
        f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    )

    caminho = f"output/{nome}"

    fundo.save(caminho)

    return jsonify({
        "status": "ok",
        "arquivo": nome,
        "url": (
            "https://all-times-copa-production.up.railway.app/imagem/"
            + nome
        )
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080
    )
