import json
from src import cache
from src.logs.logger.Logger import Logger
from flask import Blueprint, render_template, request
from src.services.consult.KabumConsultService import KabumConsultService
from src.database.query import get_products_from_database, insert_products_data

logger = Logger()

consult_blueprint = Blueprint(
    "consulta", __name__, url_prefix="/consulta-kabum")


@consult_blueprint.route("/pesquisar/<produto>", methods=["POST", "GET"])
@cache.cached(timeout=300)
def kabum_product_search(produto):
    if request.data and request.method == "POST":
        min_value = json.loads(request.data).get("valorMinimo")
        max_value = json.loads(request.data).get("valorMaximo")
        consult_service = KabumConsultService(
            min_value=int(min_value),
            max_value=int(max_value),
            search_product=produto,
            logger=logger
        )

        logger.message(f"Buscando o produto '{produto.capitalize()}' no site 'kabum.com.br'")
        consult_result = consult_service.consult_service_init()

        logger.message("Salvando no Banco de dados os resultados encontrados\n\nAguarde...")
        insert_products_data(consult_result)
        return f"""<div>
            <p style="text-align: center">Consulta finalizada com sucesso!</p>
            <p style="text-align: center">Foram encontrados {len(consult_result)} produtos relacionados à {produto.capitalize()}</p>
        </div>"""

    elif request.method == "GET":
        products_list = get_products_from_database(product=produto)
        if len(products_list) <= 0:
            return """<div><p style="text-align: center">Nenhum produto foi encontrado</p></div>"""
        return render_template("index.html", products=products_list)
