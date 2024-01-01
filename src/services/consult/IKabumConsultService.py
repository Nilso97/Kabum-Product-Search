from abc import ABC, abstractmethod


class IKabumConsultService(ABC):

    @abstractmethod
    def consult_service_init() -> None:
        raise NotImplementedError("Método 'consult_service_init' não foi implementado corretamente")
    
    @abstractmethod
    def get_consult_products():
        raise NotImplementedError("Método 'get_consult_products' não foi implementado corretamente")

    @abstractmethod
    def get_products_data(products_data: dict) -> None:
        raise NotImplementedError("Método 'get_products_data' não foi implementado corretamente")
    
    @abstractmethod
    def consult_pagination(page_number: int, total_pages: int, consult_tasks: list = []) -> None:
        raise NotImplementedError("Método 'consult_pagination' não foi implementado corretamente")
    
    @abstractmethod
    def get_consult_endpoint(page_number: int) -> str:
        raise NotImplementedError("Método 'get_consult_endpoint' não foi implementado corretamente")

    @abstractmethod
    def get_value_with_discount_prime_ninja(product: dict) -> str:
        raise NotImplementedError("Método 'get_value_with_discount_prime_ninja' não foi implementado corretamente")

    @abstractmethod
    def get_value_black_friday(product: dict) -> str:
        raise NotImplementedError("Método 'get_value_black_friday' não foi implementado corretamente")

    @abstractmethod
    def get_value_black_friday_with_discount(product: dict) -> str:
        raise NotImplementedError("Método 'get_value_black_friday_with_discount' não foi implementado corretamente")