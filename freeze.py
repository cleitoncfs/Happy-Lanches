from flask_frozen import Freezer
from app import app  # Importa o app do seu arquivo app.py

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
