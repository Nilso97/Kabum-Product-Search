from src import cache
from flask import Flask
from dotenv import load_dotenv
from src.database.DatabaseContext import db
from src.controllers.ConsultController import consult_blueprint

load_dotenv(dotenv_path="./.env")

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "SQLALCHEMY_DATABASE_URI": "sqlite:///kabum-products.db"
}

app = Flask(__name__, template_folder="templates")

app.config.from_mapping(config)

cache.init_app(app, config)

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(
    blueprint=consult_blueprint,
)