import json
import logging
import time
from core.http.RequisitionService import RequisitionService


class KabumScrapService():

    def __init__(self, search_price: int) -> None:
        self.products_list = []
        self.search_price = search_price
        self.scrap_core = RequisitionService()

        self.min_value = 1000 # Setar valor mínimo da busca

    def scrap_init(self) -> None:
        scrap_result = None
        try:
            site_response = self.scrap_core.send_http_client(
                method='GET', url='https://www.kabum.com.br/')
            if site_response is None:
                raise Exception('O site "kabum.com.br" está fora do ar!')

            print(f'Iniciando a busca por produtos no site "kabum.com.br" com valor mínimo de '+
                   f'R${self.min_value} até R${self.search_price}')
            search_url = self.get_search_url(page_number=1)
            time.sleep(5)
            response = self.scrap_core.send_http_client(
                method='GET',
                url=search_url
            )
            page_number = 2
            total_pages = json.loads(response).get('meta')['total_pages_count']
            self.get_products_data(products_data=json.loads(response))
            while total_pages >= page_number:
                print(f'Realizando a pesquisa na página {page_number} de {total_pages}')
                # time.sleep(1)
                paginate_response = self.get_consult_pagination(
                    page_number=page_number)
                self.get_products_data(
                    products_data=json.loads(paginate_response))
                page_number += 1
            self.make_product_list()
            print('Foi finalizada com sucesso a busca por produtos no site "kabum.com.br"!')
            print(f'Foram encontrados {len(self.products_list)} produtos, dentre os valores inseridos na pesquisa')
        except (Exception) as error:
            scrap_result = error
            print('Erro na função "scrap_request()" ->', str(error))
        finally:
            return scrap_result

    def make_product_list(self) -> None:
        print('Gerando arquivo ".json" contendo os produtos encontrados')
        with open("./produtos.json", "w") as file:
            json.dump(self.products_list, file, indent=4)

    def get_products_data(self, products_data: dict) -> dict:
        for product in products_data.get('data'):
            if product.get("attributes")["price"] <= self.search_price\
                    and product.get("attributes")["price"] > self.min_value:
                product_price = f'R${product.get("attributes")["price"]}'
                print(f'Foi encontrado um produto no valor de {product_price}, ' +
                      f'na página {products_data.get("meta")["page"]["number"]}')
                self.products_list.append({
                    'Id': product.get('id'),
                    'Produto': product.get('attributes')['title'],
                    'Descricao': product.get('attributes')['description'],
                    'Valor atual': product_price,
                    'Valor c/ desconto [Prime Ninja]': self.get_value_with_discount_prime_ninja(product=product),
                    'Valor [Black Friday]': self.get_value_black_friday(product=product),
                    'Valor c/ desconto [Black Friday]': self.get_value_black_friday_with_discount(product=product)
                })
        return

    def get_value_with_discount_prime_ninja(self, product: dict) -> str:
        return f'R${product.get("attributes")["prime"]["price_with_discount"]}' if product.get("attributes").get("prime") else ''

    def get_value_black_friday(self, product: dict) -> str:
        return f'R${product.get("attributes")["offer"]["price"]}' if product.get("attributes").get("offer") else ''

    def get_value_black_friday_with_discount(self, product: dict) -> str:
        return f'R${product.get("attributes")["offer"]["price_with_discount"]}' if product.get("attributes").get("offer") else ''

    def get_consult_pagination(self, page_number: int):
        paginate_response = self.scrap_core.send_http_client(
            method='GET', url=self.get_search_url(page_number=page_number))
        return paginate_response

    def get_search_url(self, page_number: int) -> str:
        paginate_url = 'https://servicespub.prod.api.aws.grupokabum.com.br'
        paginate_url += '/catalog/v2/products-by-category/computadores/notebooks?'
        paginate_url += f'page_number={page_number}&page_size=20&facet_filters=&sort=most_searched&include=gift'
        return paginate_url
