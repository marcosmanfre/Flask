from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
     return render_template('index.html')

@app.route("/cadastros")
def cadastros():
    return render_template('cadastros.html')

@app.route("/cadastros/usuario")
def usuario():
    return render_template('usuario.html', titulo="Cadastro de Usuario")

@app.route("/cadastros/caduser", methods=['POST'])
def caduser():
    return request.form

@app.route("/cadastros/anuncios")
def anuncio():
    return render_template('anuncio.html')

@app.route("/anuncios")
def anuncios():
    return render_template('anuncios.html')

@app.route("/anuncios/pergunta")
def pergunta():
    return render_template('pergunta.html')

@app.route("/anuncios/compra")
def compra():
    print("anuncio comprado")
    return "<h4> comprado </h4>"

@app.route("/anuncios/favoritos")
def favoritos():
    print("favorito inserido")
    return ""

@app.route("/config")
def config():
    return render_template('config.html')

@app.route("/config/categoria")
def categoria():
    return render_template('categoria.html')

@app.route("/relatorios")
def relatorios():
    return render_template('relatorios.html')

@app.route("/relatorios/vendas")
def relVendas():
    return render_template('relVendas.html')

@app.route("/relatorios/compras")
def relCompras():
    return render_template('relCompras.html')

