import json
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)

# Chave secreta para a sessão
app.config['SECRET_KEY'] = 'ad7ce0eb4eff3eb774dd98d84e4f0da8'

# Configuração do Banco de Dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Usuário para o banco de dados
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
# Criação das tabelas no banco de dados (se não existirem)
with app.app_context():
    db.create_all()

# Função para carregar os produtos do arquivo JSON
def load_products():
    with open('produtos.json', 'r') as file:
        products = json.load(file)
    return products

# Página inicial (redirecionamento para login se não estiver autenticado)
@app.route("/")
def homepage():
    if "user" not in session:
        return redirect(url_for("login"))
    
    produtos = load_products()
    return render_template("index.html", produtos=produtos)

@app.route("/product/<int:produto_id>")
def product(produto_id):
    produtos = load_products()
    produto = next((p for p in produtos if p["id"] == produto_id), None)
    if produto is None:
        logging.warning(f"Produto com ID {produto_id} não encontrado.")
        return render_template("404.html"), 404

    logging.info(f"Produto encontrado: {produto}")
    return render_template("product.html", produto=produto)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        
        # Verifica se o email existe no banco de dados
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Simula o envio de um e-mail (sem implementação real)
            flash(f"Um e-mail de recuperação foi enviado para {email}.", "success")
        else:
            flash("E-mail não encontrado. Tente novamente.", "danger")
        
        # Redireciona de volta ao login
        return redirect(url_for("login"))

    return render_template("forgot-password.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Consulta ao banco de dados para verificar o usuário
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session["user"] = user.email
            flash("Login bem-sucedido!", "success")
            return redirect(url_for("homepage"))
        else:
            flash("Credenciais incorretas. Tente novamente.", "danger")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("As senhas não coincidem.", "warning")
        else:
            # Criação do hash da senha
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            
            # Criação de um novo usuário e adição ao banco de dados
            new_user = User(full_name=full_name, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            
            flash("Registro concluído com sucesso! Faça login.", "success")
            return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Você saiu com sucesso.", "info")
    return redirect(url_for("login"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
