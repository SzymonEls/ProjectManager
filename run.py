import os
from app import create_app

debug = os.getenv('DEBUG', 'False') == 'True'

app = create_app()

if __name__ == '__main__':
    app.run(debug=debug)