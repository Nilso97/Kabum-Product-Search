import json
from src.config.cache.cache import cache
from flask import Blueprint, request
from src.controllers.ConsultController import ConsultController

consult_controller = ConsultController()

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
@cache.cached(timeout=3000)
def get_products(produto: str):
    return consult_controller.get_products(produto)
