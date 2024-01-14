from src import cache
from flask import Flask
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

app.register_blueprint(
    blueprint=consult_products, 
    url_prefix="/consulta-kabum"
)
