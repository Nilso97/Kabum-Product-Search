import json
from src import cache
from flask import Blueprint, request
from src.logs.logger.Logger import Logger
from src.utils.ConvertValues import ConvertValues
from src.services.consult.KabumConsultService import KabumConsultService

logger = Logger()

convert_data = ConvertValues()

consult_products = Blueprint("consulta", __name__)

@consult_products.route("/pesquisar/<produto>", methods=["POST"])
@cache.cached(timeout=300)
def kabum_product_search(produto):
    if request.data and request.method == "POST":
        min_value = convert_data.convert_values(value=json.loads(request.data).get("valorMinimo"))
        max_value = convert_data.convert_values(value=json.loads(request.data).get("valorMaximo"))
       
        logger.message(f"Buscando o produto '{produto.capitalize()}' no site 'kabum.com.br'")
        consult_service = KabumConsultService(
            min_value=min_value, 
            max_value=max_value,
            search_product=produto,
            logger=logger
        )
        consult_service.consult_service_init()
        return """<div><p style="text-align: center">Consulta finalizada com sucesso!</p></div>"""
