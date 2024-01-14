from abc import ABC, abstractmethod
from typing import Any, Coroutine, Optional


class IKabumConsultService(ABC):

    @abstractmethod
    def consult_service_init(self) -> None:
        raise NotImplementedError("Método 'consult_service_init' não foi implementado corretamente")
    
    @abstractmethod
    def get_consult_products(self):
        raise NotImplementedError("Método 'get_consult_products' não foi implementado corretamente")

    @abstractmethod
    def group_products_data(self, products_data: dict) -> Optional[Coroutine[None, Any, Any]]:
        raise NotImplementedError("Método 'group_products_data' não foi implementado corretamente")
    
    @abstractmethod
    def consult_pagination(self, page_number: int, total_pages: int, consult_tasks: list = []) -> Optional[Coroutine[None, Any, Any]]:
        raise NotImplementedError("Método 'consult_pagination' não foi implementado corretamente")
    
    @abstractmethod
    async def get_consult_endpoint(self, page_number: int) -> str:
        raise NotImplementedError("Método 'get_consult_endpoint' não foi implementado corretamente")

    @staticmethod
    async def get_value_with_discount_prime_ninja(product: dict) -> str:
        raise NotImplementedError("Método 'get_value_with_discount_prime_ninja' não foi implementado corretamente")

    @staticmethod
    async def get_value_black_friday(product: dict) -> str:
        raise NotImplementedError("Método 'get_value_black_friday' não foi implementado corretamente")

    @staticmethod
    async def get_value_black_friday_with_discount(product: dict) -> str:
        raise NotImplementedError("Método 'get_value_black_friday_with_discount' não foi implementado corretamente")