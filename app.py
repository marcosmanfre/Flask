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
    __tablename__ = "usuario"
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

class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column('cat_id', db.Integer, primary_key=True)
    nome = db.Column('cat_nome', db.String(256))

    def __init__ (self, nome, desc):
        self.nome = nome

class Anuncio(db.Model):
    __tablename__ = "anuncio"
    id = db.Column('anu_id', db.Integer, primary_key=True)
    nome = db.Column('anu_nome', db.String(256))
    desc = db.Column('anu_desc', db.String(256))
    qtd = db.Column('anu_qtd', db.Integer)
    preco = db.Column('anu_preco', db.Float)
    cat_id = db.Column('cat_id',db.Integer, db.ForeignKey("categoria.cat_id"))
    usu_id = db.Column('usu_id',db.Integer, db.ForeignKey("usuario.usu_id"))

    def __init__ (self, nome, desc, qtd, preco, cat_id, usu_id):
        self.nome = nome
        self.desc = desc
        self.qtd = qtd
        self.preco = preco
        self.cat_id = cat_id
        self.usu_id = usu_id


class Pergunta(db.Model):
    __tablename__ = "pergunta"
    id = db.Column('per_id', db.Integer, primary_key=True)
    anu_id = db.Column('anu_id',db.Integer, db.ForeignKey("anuncio.anu_id"))
    usu_id = db.Column('usu_id',db.Integer, db.ForeignKey("usuario.usu_id"))
    perguntas = db.Column('per_pergunta', db.String(256))
    respostas = db.Column('per_resposta', db.String(256))


    def __init__ (self, anu_id, usu_id, per_pergunta, per_resposta):
        self.anu_id = anu_id
        self.usu_id = usu_id
        self.per_pergunta = per_pergunta
        self.per_resposta = per_resposta
       

class Favorito(db.Model):
    __tablename__ = "favorito"
    fav_id = db.Column('fav_id', db.Integer, primary_key=True)
    anu_id = db.Column('anu_id',db.Integer, db.ForeignKey("anuncio.anu_id"))
    usu_id = db.Column('usu_id',db.Integer, db.ForeignKey("usuario.usu_id"))


    def __init__ (self, anu_id, usu_id, ):
        self.anu_id = anu_id
        self.usu_id = usu_id


class Compra(db.Model):
    __tablename__ = "Compra"
    com_id = db.Column('com_id', db.Integer, primary_key=True)
    com_qtd = db.Column('com_qtd', db.Integer)
    com_preco = db.Column('com_preco', db.Integer)
    com_total = db.Column('com_total', db.Integer)
    anu_id = db.Column('anu_id',db.Integer, db.ForeignKey("anuncio.anu_id"))
    usu_id = db.Column('usu_id',db.Integer, db.ForeignKey("usuario.usu_id"))


    def __init__ (self, com_id, com_qtd, com_preco, com_total, anu_id, usu_id):
        self.com_id = com_id
        self.com_qtd = com_qtd
        self.com_preco = com_preco
        self.com_total = com_total
        self.anu_id = anu_id
        self.usu_id = usu_id


@app.errorhandler(404)
def paginanaoencontrada(error):
    return render_template('paginanaoencontrada.html')

@app.route("/")
def index():
     return render_template('index.html')

@app.route("/cadastros")
def cadastros():
    return render_template('cadastros.html')

@app.route("/cadastros/usuario")
def usuario():
    return render_template('usuario.html', usuarios = Usuario.query.all(), titulo="Cadastro de Usuário")


@app.route("/usuario/criar", methods=['POST'])
def criarusuario():
    usuario = Usuario(request.form.get('user'),request.form.get('email'),request.form.get('passwd'),request.form.get('end'))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))

@app.route("/usuario/detalhar/<int:id>")
def buscarusuario(id):
    usuario = Usuario.query.get(id)
    return usuario.nome

@app.route("/usuario/editar/<int:id>", methods=['GET','POST'])
def editarusuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('user')
        usuario.email = request.form.get('email')
        usuario.senha = request.form.get('passwd')
        usuario.end = request.form.get('end')
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('usuario'))
    
    return render_template('eusuario.html', usuario = usuario, titulo="Usuario")

@app.route("/usuario/deletar<int:id>")
def deletarusuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))


@app.route("/cadastros/anuncio")
def anuncio():
    return render_template('anuncio.html', anuncios = Anuncio.query.all(), categorias = Categoria.query.all(), titulo="Anuncio")

@app.route("/anuncios")
def anuncios():
    return render_template('anuncios.html')


@app.route("/anuncio/novo", methods=['POST'])
def novoanuncio():
    anuncio = Anuncio(request.form.get('nome'), request.form.get('desc'),request.form.get('qtd'),request.form.get('preco'),request.form.get('cat'),request.form.get('usu'))
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for('anuncio'))

@app.route("/anuncio/editar/<int:id>", methods=['GET','POST'])
def editaranuncio(id):
    anuncio = Anuncio.query.get(id)
    if request.method == 'POST':
        anuncio.nome = request.form.get('nome')
        anuncio.desc = request.form.get('desc')
        anuncio.qtd = request.form.get('qtd')
        anuncio.preco = request.form.get('preco')
        anuncio.cat = request.form.get('cat')
        anuncio.usu = request.form.get('usu')
        db.session.add(anuncio)
        db.session.commit()
        return redirect(url_for('anuncio'))
    
    return render_template('edianuncio.html', anuncio = anuncio, titulo="Anuncio")

@app.route("/anuncio/deletar<int:id>")
def deletaranuncio(id):
    anuncio = Anuncio.query.get(id)
    db.session.delete(anuncio)
    db.session.commit()
    return redirect(url_for('anuncio'))
    


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
    return render_template('categoria.html', categorias = Categoria.query.all(), titulo='Categoria')

@app.route("/categoria/novo", methods=['POST'])
def novacategoria():
    categoria = Categoria(request.form.get('nome'), request.form.get('desc'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))

@app.route("/categoria/editar/<int:id>", methods=['GET','POST'])
def editarcategoria(id):
    categoria = Categoria.query.get(id)
    if request.method == 'POST':
        categoria.nome = request.form.get('nome')
        categoria.desc = request.form.get('desc')
        db.session.add(categoria)
        db.session.commit()
        return redirect(url_for('categoria'))
    
    return render_template('edicategoria.html', categoria = categoria, titulo="Categoria")

@app.route("/categoria/deletar<int:id>")
def deletarcategoria(id):
    categoria = Categoria.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))

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
  


