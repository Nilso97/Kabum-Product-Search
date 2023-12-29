from flask import Flask
from flask_caching import Cache
from src.controllers.ConsultController import consult_products

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})

app = Flask(__name__)

app.config.from_mapping(config)

cache = Cache(app)

cache.init_app(app)

app.register_blueprint(consult_products)
