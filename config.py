import os
from dotenv import load_dotenv
from app.extensions import db
from flask_migrate import upgrade

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    ENV_FILE = ".env"
    ENV_EXAMPLE_FILE = ".env.example"
    DB_DIR = "db"
    if not os.path.exists(ENV_FILE) and os.path.exists(ENV_EXAMPLE_FILE):
        with open(ENV_EXAMPLE_FILE, 'r') as src_file:
            with open(ENV_FILE, 'w') as dst_file:
                dst_file.write(src_file.read())
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

    load_dotenv(override=True)
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY') or os.urandom(32).hex()
    FLASK_ENV = os.getenv('FLASK_ENV')
    FLASK_APP = os.getenv('FLASK_APP')
    DEBUG = os.getenv('DEBUG')
    REGISTER = os.getenv('REGISTER')
    AUTOMATIC_DB_CREATION = int(os.getenv('AUTOMATIC_DB_CREATION'))
    #DB_USER = os.getenv('DB_USER', 'root')
    #DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    #DB_HOST = os.getenv('DB_HOST', 'localhost')
    #DB_PORT = os.getenv('DB_PORT', '3306')
    #DB_NAME = os.getenv('DB_NAME', 'test')
    #SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"\
    #    or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False