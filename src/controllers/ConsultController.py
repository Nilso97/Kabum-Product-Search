import json
from flask import Blueprint, request
from src.logs.logger.Logger import Logger
from src.utils.ConvertData import ConvertData
from src.email.EmailService import EmailService
from src.services.KabumConsultService import KabumConsultService

logger = Logger()

convert_data = ConvertData()

email_service = EmailService()

consult_products = Blueprint("consulta", __name__, url_prefix="/consulta-kabum")

@consult_products.route("/pesquisar/<produto>", methods=["POST"])
def kabum_product_search(produto) -> None:
    if request.data and request.method == "POST":
        json_data = json.loads(request.data)
        logger.information(f"Buscando o produto '{produto.capitalize()}' no site 'kabum.com.br'")
        min_value = convert_data.converted_values(value=json_data.get("valorMinimo"))
        max_value = convert_data.converted_values(value=json_data.get("valorMaximo"))
        consult_service = KabumConsultService(
            min_value=min_value, 
            max_value=max_value,
            search_product=produto
        )
        consult_service.consult_service_init()
        email_service.send_email()
        return """
            <div>
                <p style="text-align: center">Consulta finalizada com sucesso!</p>
            </div>
        """
