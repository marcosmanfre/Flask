from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:marcos123@localhost:3306/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column('usu_id', db.Integer, primary_key=True)
    nome = db.Column('usu_nome', db.String(256))
    email = db.Column('usu_email', db.String(256))
    senha = db.Column('usu_senha', db.String(256))
    end = db.Column('usu_end', db.String(256))

    def __init__(self, nome, email, senha, end):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.end = end

@app.route("/")
def index():
     return render_template('index.html')

@app.route("/cadastros")
def cadastros():
    return render_template('cadastros.html')

@app.route("/cadastros/usuario")
def cadusuario():
    return render_template('usuario.html', usuarios = Usuario.query.all(), titulo="Cadastro de Usuário")


@app.route("/cadastros/caduser", methods=['POST'])
def caduser():
    usuario = Usuario(request.form.get('user'),request.form.get('email'),request.form.get('passwd'),request.form.get('end'))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('cadusuario'))

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

if __name__ == 'app':  
    db.create_all()
  


