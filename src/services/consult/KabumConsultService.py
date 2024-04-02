import json
import httpx
import asyncio
import requests
from typing import Optional, Type
from src.logs.logger.ILogger import ILogger
from src.email.EmailService import EmailService
from src.core.sheets.SheetsCore import SheetsCore
from src.services.consult.IKabumConsultService import IKabumConsultService


class KabumConsultService(IKabumConsultService):

    def __init__(
        self,
        min_value: int,
        max_value: int,
        category: str,
        search_product: str,
        logger: Type[ILogger]
    ) -> None:
        self.logger = logger
        self.min_value = min_value
        self.max_value = max_value
        self.category = category
        self.search_product = search_product
        self.sheets_core = SheetsCore(
            logger=self.logger
        )
        self.email_service = EmailService(
            logger=self.logger
        )
        self.products_list: list = []
        self.base_url: str = "https://servicespub.prod.api.aws.grupokabum.com.br"

    def consult_service_init(self) -> list[dict]:
        asyncio.run(self.consult_products())

        return self.products_list

    async def consult_products(self) -> None:
        self.logger.message(f"Buscando produtos no site 'kabum.com.br' com valor entre R${self.min_value} até R${self.max_value}")
        try:
            consult_response = requests.get(
                url=await self.make_consult_endpoint(page_number=1)
            )

            await self.group_products_data(products_data=json.loads(consult_response.text))

            total_pages = json.loads(consult_response.text).get("meta")["total_pages_count"]
            if total_pages > 1:
                await self.consult_pagination(
                    page_number=2,
                    total_pages=total_pages
                )

            if len(self.products_list) > 0:
                self.sheets_core.create_xlsx(products_list=self.products_list)
                self.logger.message(f"Foram encontrados {len(self.products_list)} produtos, dentre os valores inseridos na pesquisa")
                self.logger.message("Finalizada com sucesso a busca por produtos no site 'kabum.com.br'")

                self.logger.message("Enviando e-mail contendo a planilha com os produtos encontrados\n\nAguarde...")
                # self.email_service.send_email()
            else:
                self.logger.message("Nenhum produto encontrado para os valores inseridos na pesquisa")
                return

        except (Exception) as error:
            self.logger.error(f"Erro durante a busca por produtos no site da Kabum: {error}")

    async def group_products_data(self, products_data: dict) -> None:
        for product in products_data["data"]:
            if (
                product.get("attributes")["price"] <= self.max_value
                and product.get("attributes")["price"] > self.min_value
            ):
                self.logger.message(
                    f"Foi encontrado um produto no valor de "
                    + f"R${product['attributes']['price']}, na página {products_data['meta']['page']['number']}"
                )

                self.products_list.append({
                    "Id": int(product.get("id")),
                    "Produto": product.get("attributes")["title"],
                    "Descricao": product.get("attributes")["description"],
                    "Valor atual": int(product.get('attributes')['price']),
                    "Valor com desconto [Prime Ninja]": await self.get_price_with_discount_prime_ninja(product=product),
                    "Valor [Black Friday]": await self.get_price_black_friday(product=product),
                    "Valor com desconto [Black Friday]": await self.get_price_black_friday_with_discount(product=product)
                })

    async def consult_pagination(self, page_number: int, total_pages: int, consult_tasks: list = []) -> None:
        async with httpx.AsyncClient(timeout=3000, follow_redirects=True) as client:
            for page_number in range(2, total_pages):
                self.logger.message(f"Realizando a busca por produtos na página {page_number} de {total_pages}")
                consult_response = await client.get(
                    url=await self.make_consult_endpoint(page_number=page_number),
                    headers={
                        "Accept": "application/json, text/plain, */*",
                        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6"
                    }
                )
                if consult_response and (consult_response.status_code == 200):
                    consult_tasks.append(
                        self.group_products_data(
                            products_data=json.loads(consult_response.text)
                        )
                    )

            await asyncio.gather(*consult_tasks)

    async def make_consult_endpoint(self, page_number: int) -> str:
        consult_endpoint = f"{self.base_url}/catalog/v2/products-by-category/{self.category}/{self.search_product}?"
        consult_endpoint += f"page_number={page_number}&page_size=20&facet_filters=&sort=most_searched&include=gift"

        return consult_endpoint

    @staticmethod
    async def get_price_with_discount_prime_ninja(product: dict) -> Optional[int]:
        return int(product['attributes']['prime']['price_with_discount']) if product["attributes"].get("prime") else None

    @staticmethod
    async def get_price_black_friday(product: dict) -> Optional[int]:
        return int(product['attributes']['offer']['price']) if product["attributes"].get("offer") else None

    @staticmethod
    async def get_price_black_friday_with_discount(product: dict) -> Optional[int]:
        return int(product['attributes']['offer']['price_with_discount']) if product["attributes"].get("offer") else None
