import json
import time
import httpx
import asyncio
from src.core.sheets.SheetsCore import SheetsCore
from src.core.http.RequisitionService import RequisitionService
from src.logs.logger.Logger import Logger
from src.services.IKabumConsultService import IKabumConsultService


class KabumConsultService(IKabumConsultService):

    def __init__(
        self, 
        min_value: int, 
        max_value: int, 
        search_product: str
    ) -> None:
        self.logger = Logger()
        self.products_list = []
        self.min_value = min_value
        self.max_value = max_value
        self.search_product = search_product
        self.http_request = RequisitionService()
        self.sheets_core = SheetsCore()

    def consult_service_init(self) -> None:
        asyncio.run(self.get_consult_products())
    
    async def get_consult_products(self) -> None:
        """"""
        try:
            self.logger.information('Iniciando a busca por produtos no site "kabum.com.br" com valor mínimo de ' +
                                      f'R${self.min_value} até R${self.max_value}')
            time.sleep(2)
            search_url = await self.get_consult_endpoint(page_number=1)

            initial_response = self.http_request.send_http_client(
                method='get',
                url=search_url,
                body=None
            )
            await self.get_products_data(products_data=json.loads(initial_response))
            total_pages = json.loads(initial_response).get('meta')['total_pages_count']
            if total_pages > 1:
                await self.consult_pagination(
                    page_number=2, 
                    total_pages=total_pages
                )

            if len(self.products_list) > 0:
                self.sheets_core.create_xlsx(products_list=self.products_list)
                self.logger.information(f'Foram encontrados {len(self.products_list)} produtos, dentre os valores inseridos na pesquisa')
                self.logger.information('Finalizada com sucesso a busca por produtos no site "kabum.com.br"')
            else:
                self.logger.information('Nenhum produto encontrado para os valores inseridos na pesquisa')
                return
        except (Exception) as error:
            self.logger.error(f'Erro durante a busca por produtos no site da Kabum: {error}')

    async def get_products_data(self, products_data: dict) -> None:
        """"""
        for product in products_data.get('data'):
            if product.get("attributes")["price"] <= self.max_value\
                    and product.get("attributes")["price"] > self.min_value:
                product_price = f'R${product.get("attributes")["price"]}'
                self.logger.information(f'Foi encontrado um produto no valor de {product_price}, ' +
                                          f'na página {products_data.get("meta")["page"]["number"]}')
                self.products_list.append({
                    'Id': product.get('id'),
                    'Produto': product.get('attributes')['title'],
                    'Descricao': product.get('attributes')['description'],
                    'Valor atual': product_price,
                    'Valor com desconto [Prime Ninja]': await self.get_value_with_discount_prime_ninja(product=product),
                    'Valor [Black Friday]': await self.get_value_black_friday(product=product),
                    'Valor com desconto [Black Friday]': await self.get_value_black_friday_with_discount(product=product)
                })
    
    async def consult_pagination(self, page_number: int, total_pages: int) -> None:
        """"""
        consult_tasks = []
        try:
            async with httpx.AsyncClient(timeout=3000, follow_redirects=True) as client:
                for page_number in range(2, total_pages):
                    self.logger.information(f'Realizando a pesquisa na página {page_number} de {total_pages}')
                    paginate_response = await client.get(
                        url=await self.get_consult_endpoint(page_number=page_number)
                    )
                    if paginate_response and (paginate_response.status_code == 200):
                        consult_tasks.append(
                            self.get_products_data(
                                products_data=json.loads(paginate_response.text)
                            )
                        )
                await asyncio.gather(*consult_tasks)
        except (Exception) as error:
            error_message = str(error)
            self.logger.error( f'Erro na função "consult_pagination()" -> {error_message}')
    
    async def get_consult_endpoint(self, page_number: int) -> str:
        """"""
        endpoint = 'https://servicespub.prod.api.aws.grupokabum.com.br'
        endpoint += f'/catalog/v2/products-by-category/celular-smartphone/smartphones/{self.search_product}?'
        endpoint += f'page_number={page_number}&page_size=20&facet_filters=&sort=most_searched&include=gift'
        return endpoint
  
    async def get_value_with_discount_prime_ninja(self, product: dict) -> str:
        return f'R${product.get("attributes")["prime"]["price_with_discount"]}'\
            if product.get("attributes").get("prime") else 'Não possui desconto com o Prime Ninja'

    async def get_value_black_friday(self, product: dict) -> str:
        return f'R${product.get("attributes")["offer"]["price"]}'\
            if product.get("attributes").get("offer") else 'Não foi possível obter o valor da Black Friday'

    async def get_value_black_friday_with_discount(self, product: dict) -> str:
        return f'R${product.get("attributes")["offer"]["price_with_discount"]}'\
            if product.get("attributes").get("offer") else 'Não foi possível obter o valor da Black Friday c/ desconto'
