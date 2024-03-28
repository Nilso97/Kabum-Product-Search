import json
from src.cache.cache import cache
from flask import Blueprint, request
from src.controllers.ConsultController import ConsultController

consult_controller = ConsultController()

consult_blueprint = Blueprint("consult_blueprint", __name__, url_prefix="/consulta-kabum")

@consult_blueprint.route("/pesquisar/<produto>", methods=["POST"])
@cache.cached(timeout=5000)
def search_products(produto: str):
    return consult_controller.search_products(
        produto,
        json.loads(request.data).get("valorMinimo"),
        json.loads(request.data).get("valorMaximo")
    )

@consult_blueprint.route("/produtos/<produto>", methods=["GET"])
@cache.cached(timeout=3000)
def get_products(produto: str):
    return consult_controller.get_products(produto)
