from flask import Flask
from dotenv import load_dotenv
from src.cache.cache import cache
from src.config.config import config
from src.database.DatabaseContext import db
from src.routes.routes import consult_blueprint

load_dotenv(".env")

app = Flask(__name__, template_folder="templates")

app.register_blueprint(blueprint=consult_blueprint)

app.config.from_mapping(config)

cache.init_app(app, config)

db.init_app(app)

with app.app_context():
    db.create_all()
