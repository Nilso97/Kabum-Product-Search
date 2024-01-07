import json
import httpx
import asyncio
from src.logs.logger.ILogger import ILogger
from typing import Any,Coroutine, Optional, Type
from src.core.sheets.SheetsCore import SheetsCore
from src.services.email.EmailService import EmailService
from src.core.http.RequisitionService import RequisitionService
from src.services.consult.IKabumConsultService import IKabumConsultService


class KabumConsultService(IKabumConsultService):

    def __init__(
        self, 
        min_value: int, 
        max_value: int, 
        search_product: str,
        logger: Type[ILogger]
    ) -> None:
        self.logger = logger
        self.min_value = min_value
        self.max_value = max_value
        self.search_product = search_product
        self.http_request = RequisitionService(logger=self.logger)
        self.sheets_core = SheetsCore(
            logger=self.logger,
        )
        self.email_service = EmailService(
            logger=self.logger, 
        )
        self.__products_list: list = []

    def consult_service_init(self) -> None:
        asyncio.run(self.get_consult_products())
    
    async def get_consult_products(self) -> None:
        try:
            self.logger.message("Iniciando a busca por produtos no site 'kabum.com.br' com valor mínimo de " +
                                      f"R${self.min_value} até R${self.max_value}")
            product_search_url = await self.get_consult_endpoint(page_number=1)
            consult_response = self.http_request.send_http_client(
                method='get',
                url=product_search_url,
                body={}
            )

            await self.group_products_data(
                products_data=json.loads(consult_response)
            )
            total_pages = json.loads(consult_response).get("meta")["total_pages_count"]
            if total_pages > 1:
                await self.consult_pagination(
                    page_number=2, 
                    total_pages=total_pages
                )

            if len(self.__products_list) > 0:
                self.sheets_core.create_xlsx(products_list=self.__products_list)
                self.logger.message(
                    f"Foram encontrados {len(self.__products_list)} produtos, dentre os valores inseridos na pesquisa")
                self.logger.message("Finalizada com sucesso a busca por produtos no site 'kabum.com.br'")
                self.email_service.send_email()
            else:
                self.logger.message("Nenhum produto encontrado para os valores inseridos na pesquisa")
                return
        except (Exception) as error:
            error_message = str(error)
            self.logger.error(
                f"Erro durante a busca por produtos no site da Kabum: {error_message}")

    async def group_products_data(self, products_data: dict) -> Optional[Coroutine[None, Any, Any]]:
        for product in products_data["data"]:
            if product.get("attributes")["price"] <= self.max_value:
                if product.get("attributes")["price"] > self.min_value:
                    self.logger.message(
                        f"Foi encontrado um produto no valor de " +
                        f"R${product['attributes']['price']}, na página {products_data['meta']['page']['number']}"
                    )
                    self.__products_list.append({
                        "Id": product.get("id"),
                        "Produto": product.get("attributes")["title"],
                        "Descricao": product.get("attributes")["description"],
                        "Valor atual": f"R${product.get('attributes')['price']}",
                        "Valor com desconto [Prime Ninja]": await self.get_value_with_discount_prime_ninja(product=product),
                        "Valor [Black Friday]": await self.get_value_black_friday(product=product),
                        "Valor com desconto [Black Friday]": await self.get_value_black_friday_with_discount(product=product)
                    })
        return None
    
    async def consult_pagination(self, page_number: int, total_pages: int, consult_tasks: list = []) -> Optional[Coroutine[None, Any, Any]]:
        try:
            async with httpx.AsyncClient(timeout=3000, follow_redirects=True) as client:
                for page_number in range(2, total_pages):
                    self.logger.message(f"Realizando a busca por produtos na página {page_number} de {total_pages}")
                    consult_url = await self.get_consult_endpoint(page_number=page_number)
                    paginate_response = await client.get(
                        url=consult_url,
                        headers={
                            "Accept": "application/json, text/plain, */*",
                            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6",
                            "Sec-Fetch-Mode": "cors",
                            "Sec-Fetch-Site": "cross-site"
                        }
                    )
                    if paginate_response and (paginate_response.status_code == 200):
                        consult_tasks.append(
                            self.group_products_data(
                                products_data=json.loads(paginate_response.text)
                            )
                        )
                await asyncio.gather(*consult_tasks)
        except (Exception) as error:
            error_message = str(error)
            self.logger.error(
                f"Erro durante a busca por produtos na página {page_number}: {error_message}")
        finally:
            return None
    
    async def get_consult_endpoint(self, page_number: int) -> str:
        endpoint = "https://servicespub.prod.api.aws.grupokabum.com.br"
        endpoint += f"/catalog/v2/products-by-category/computadores/monitores/{self.search_product}?"
        endpoint += f"page_number={page_number}&page_size=20&facet_filters=&sort=most_searched&include=gift"
        return endpoint
    
    @staticmethod
    async def get_value_with_discount_prime_ninja(product: dict) -> str:
        return f"R${product['attributes']['prime']['price_with_discount']}" if product["attributes"].get("prime") else ""

    @staticmethod
    async def get_value_black_friday(product: dict) -> str:
        return f"R${product['attributes']['offer']['price']}" if product["attributes"].get("offer") else ""

    @staticmethod
    async def get_value_black_friday_with_discount(product: dict) -> str:
        return f"R${product['attributes']['offer']['price_with_discount']}" if product["attributes"].get("offer") else ""