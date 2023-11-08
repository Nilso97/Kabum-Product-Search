import json
import time
from core.http.RequisitionService import RequisitionService
from core.logger.LoggerService import LoggerService


class KabumScrapService():

    def __init__(self, min_value: any, max_value: any) -> None:
        self.products_list = []
        self.min_value = int(min_value)
        self.max_value = int(max_value)
        self.scrap_core = RequisitionService()
        self.logger = LoggerService()

    def scrap_init(self) -> None:
        """"""
        scrap_result = None
        try:
            self.__default_message = 'Kabum WebScraping Service -'
            self.logger.send_info_msg(f'{self.__default_message} Iniciando a busca por produtos no site "kabum.com.br" com valor mínimo de ' +
                                      f'R${self.min_value} até R${self.max_value}')
            time.sleep(5)
            search_url = self.get_default_endpoint(page_number=1)

            response = self.scrap_core.send_http_client(
                method='get',
                url=search_url,
                body=None
            )
            self.get_products_data(products_data=json.loads(response))
            total_pages = json.loads(response).get('meta')['total_pages_count']
            if total_pages > 1:
                self.get_search_pagination(
                    page_number=2, total_pages=total_pages)

            if len(self.products_list) > 0:
                self.make_products_json()
            else:
                self.logger.send_info_msg(
                    f'{self.__default_message} Nenhum produto encontrado para os valores inseridos na pesquisa')
                return scrap_result

            self.logger.send_info_msg(
                f'{self.__default_message} Foram encontrados {len(self.products_list)} produtos, dentre os valores inseridos na pesquisa')
            self.logger.send_info_msg(
                f'{self.__default_message} Finalizada com sucesso a busca por produtos no site "kabum.com.br"')
        except (Exception) as error:
            scrap_result = str(error)
            self.logger.send_error_msg(
                f'Erro na função "scrap_request()" -> {scrap_result}')
        finally:
            return scrap_result

    def make_products_json(self) -> None:
        """"""
        try:
            self.logger.send_info_msg(
                f'{self.__default_message} Gerando arquivo ".json" contendo os produtos encontrados')
            with open("./produtos.json", "w") as file:
                json.dump(self.products_list, file, indent=4)
        except (Exception) as error:
            error_message = str(error)
            self.logger.send_error_msg(f'Erro na função "make_product_json()" -> {error_message}')

    def get_products_data(self, products_data: dict) -> None:
        """"""
        for product in products_data.get('data'):
            if product.get("attributes")["price"] <= self.max_value\
                    and product.get("attributes")["price"] > self.min_value:
                product_price = f'R${product.get("attributes")["price"]}'
                self.logger.send_info_msg(f'{self.__default_message} Foi encontrado um produto no valor de {product_price}, ' +
                                          f'na página {products_data.get("meta")["page"]["number"]}')
                self.products_list.append({
                    'Id': product.get('id'),
                    'Produto': product.get('attributes')['title'],
                    'Descricao': product.get('attributes')['description'],
                    'Valor atual': product_price,
                    'Valor com desconto [Prime Ninja]': self.get_value_with_discount_prime_ninja(product=product),
                    'Valor [Black Friday]': self.get_value_black_friday(product=product),
                    'Valor com desconto [Black Friday]': self.get_value_black_friday_with_discount(product=product)
                })

    def get_search_pagination(self, page_number: int, total_pages: int) -> str:
        """"""
        try:
            while total_pages >= page_number:
                self.logger.send_info_msg(
                    f'{self.__default_message} Realizando a pesquisa na página {page_number} de {total_pages}')
                time.sleep(1)
                paginate_response = self.scrap_core.send_http_client(
                    method='get', url=self.get_default_endpoint(page_number=page_number), body=None)
                self.get_products_data(
                    products_data=json.loads(paginate_response))
                page_number += 1
        except (Exception) as error:
            paginate_response = str(error)
            self.logger.send_error_msg( f'Erro na função "get_search_pagination()" -> {paginate_response}')
        finally:
            return paginate_response

    def get_default_endpoint(self, page_number: int) -> str:
        """"""
        default_endpoint = 'https://servicespub.prod.api.aws.grupokabum.com.br'
        default_endpoint += '/catalog/v2/products-by-category/computadores/notebooks?'
        default_endpoint += f'page_number={page_number}&page_size=20&facet_filters=&sort=most_searched&include=gift'
        return default_endpoint

    def get_value_with_discount_prime_ninja(self, product: dict) -> str:
        return f'R${product.get("attributes")["prime"]["price_with_discount"]}'\
            if product.get("attributes").get("prime") else 'Não possui desconto com o Prime Ninja'

    def get_value_black_friday(self, product: dict) -> str:
        return f'R${product.get("attributes")["offer"]["price"]}'\
            if product.get("attributes").get("offer") else 'Não foi possível obter o valor da Black Friday'

    def get_value_black_friday_with_discount(self, product: dict) -> str:
        return f'R${product.get("attributes")["offer"]["price_with_discount"]}'\
            if product.get("attributes").get("offer") else 'Não foi possível obter o valor da Black Friday c/ desconto'
    
    def get_products_category(self):
        """Mapear algumas das principais categorias"""
        # TODO mapear algumas das principais categorias
        pass

    def make_formated_endpoint(self):
        """Formatar/Montar o endpoint com base na categoria selecionada"""
        # TODO formatar o endpoint com base na categoria selecionada
        pass
