from flask import Flask
from src.cache import cache
from dotenv import load_dotenv
from src.controllers.ConsultController import consult_products

load_dotenv(dotenv_path="./.env")

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)

app.config.from_mapping(config)

cache.init_app(app, config)

app.register_blueprint(consult_products)
