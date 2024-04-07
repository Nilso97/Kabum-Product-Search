from typing import Type
from flask import render_template
from src.logs.logger.ILogger import ILogger
from src.services.ProductDataService import ProductDataService
from src.services.consult.KabumConsultService import KabumConsultService


class ConsultController:

    def __init__(self, logger: Type[ILogger]) -> None:
        self.logger = logger
        self.product_data_service = ProductDataService()

    def get_products(self, product: str):
        products_data_list = self.product_data_service.get_products_data(product)
        if len(products_data_list) <= 0:
            return """<div><p style="text-align: center">Nenhum produto foi encontrado</p></div>"""

        return render_template("index.html", products=products_data_list)

    def search_products(self, category: str, product: str, min_value: str, max_value: str):
        consult_service = KabumConsultService(
            min_value=int(min_value),
            max_value=int(max_value),
            category=category,
            search_product=product,
            logger=self.logger
        )

        self.logger.message(f"Buscando o produto '{product.capitalize()}' no site 'kabum.com.br'")
        consult_result = consult_service.consult_service_init()

        self.logger.message("Salvando no Banco de dados os resultados encontrados\n\nAguarde...")
        self.product_data_service.save_products_data(consult_result)

        return f"""<div>
            <p style="text-align: center">Consulta finalizada com sucesso!</p>
            <p style="text-align: center">Foram encontrados {len(consult_result)} produtos relacionados à {product.capitalize()}</p>
        </div>"""
