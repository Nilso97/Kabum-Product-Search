import json
from flask import Blueprint, request
from src.logs.logger.Logger import Logger
from src.utils.ConvertValues import ConvertValues
from src.services.consult.KabumConsultService import KabumConsultService

logger = Logger()

convert_data = ConvertValues()

consult_products = Blueprint("consulta", __name__, url_prefix="/consulta-kabum")

@consult_products.route("/pesquisar/<produto>", methods=["POST"])
def kabum_product_search(produto) -> str:
    if request.data and request.method == "POST":
        json_data = json.loads(request.data)
        logger.information(f"Buscando o produto '{produto.capitalize()}' no site 'kabum.com.br'")
        min_value = convert_data.convert_values(value=json_data.get("valorMinimo"))
        max_value = convert_data.convert_values(value=json_data.get("valorMaximo"))
        consult_service = KabumConsultService(
            min_value=min_value, 
            max_value=max_value,
            search_product=produto,
            logger=logger
        )
        consult_service.consult_service_init()
        return """<div><p style="text-align: center">Consulta finalizada com sucesso!</p></div>"""
