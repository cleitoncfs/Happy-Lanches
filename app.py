import json
import logging
from flask import Flask, render_template

app = Flask(__name__)

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)

# Função para carregar os produtos do arquivo JSON
def load_products():
    with open('produtos.json', 'r') as file:
        products = json.load(file)
    return products

@app.route("/")
def homepage():
    produtos = load_products()
    return render_template("index.html", produtos=produtos)

@app.route("/product/<int:produto_id>")
def product(produto_id):
    produtos = load_products()
    produto = next((p for p in produtos if p["id"] == produto_id), None)
    if produto is None:
        logging.warning(f"Produto com ID {produto_id} não encontrado.")
        return render_template("404.html"), 404  # Renderiza uma página 404 personalizada

    logging.info(f"Produto encontrado: {produto}")
    return render_template("product.html", produto=produto)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/forgot-password")
def forgot_password():
    return render_template("forgot-password.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Não executar caso seja importação.
if __name__ == "__main__":
    app.run(debug=True)
