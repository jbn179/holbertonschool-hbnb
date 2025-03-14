import sys
import os

# Ajouter le répertoire courant au chemin Python
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from hbnb.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)