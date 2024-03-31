from flask import render_template
from src.logs.logger.Logger import Logger
from src.repository.ProductRepository import ProductRepository
from src.services.consult.KabumConsultService import KabumConsultService


class ConsultController:

    def __init__(self) -> None:
        self.logger = Logger()
        self.__product_repository = ProductRepository()

    def get_products(self, product: str):
        products_list = self.__product_repository.get_products_from_database(product)
        if len(products_list) <= 0:
            return """<div><p style="text-align: center">Nenhum produto foi encontrado</p></div>"""
        
        return render_template("index.html", products=products_list)

    def search_products(self, product: str, min_value: str, max_value: str):
        consult_service = KabumConsultService(
            min_value=int(min_value),
            max_value=int(max_value),
            search_product=product,
            logger=self.logger
        )
        
        self.logger.message(f"Buscando o produto '{product.capitalize()}' no site 'kabum.com.br'")
        consult_result = consult_service.consult_service_init()
        
        self.logger.message("Salvando no Banco de dados os resultados encontrados\n\nAguarde...")
        self.__product_repository.insert_products_data(consult_result)
        
        return f"""<div>
            <p style="text-align: center">Consulta finalizada com sucesso!</p>
            <p style="text-align: center">Foram encontrados {len(consult_result)} produtos relacionados à {product.capitalize()}</p>
        </div>"""
