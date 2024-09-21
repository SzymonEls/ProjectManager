from app import create_app
from app.extensions import db
from flask_migrate import Migrate
from config import Config

app = create_app(Config)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()