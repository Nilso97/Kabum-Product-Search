import json
from flask import Blueprint, request
from src.config.cache.cache import cache
from src.logs.logger.Logger import Logger
from src.controllers.ConsultController import ConsultController

consult_controller = ConsultController(Logger())

consult_blueprint = Blueprint("consult_blueprint", __name__, url_prefix="/consulta-kabum")


@consult_blueprint.route("/pesquisar/<category>/<product>", methods=["POST"])
def search_products(category: str, product: str):
    return consult_controller.search_products(
        category=category,
        product=product,
        min_value=json.loads(request.data).get("valorMinimo"),
        max_value=json.loads(request.data).get("valorMaximo")
    )


@consult_blueprint.route("/produtos/<produto>", methods=["GET"])
@cache.cached(timeout=300)
def get_products(produto: str):
    return consult_controller.get_products(produto)
