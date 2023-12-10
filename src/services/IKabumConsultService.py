from abc import ABC, abstractmethod


class IKabumConsultService(ABC):

    @abstractmethod
    def consult_service_init() -> None:
        raise NotImplementedError('Método "consult_service_init" não implementado')
    
    @abstractmethod
    def get_consult_products():
        raise NotImplementedError('Método "get_consult_products" não implementado')

    @abstractmethod
    def make_products_json() -> None:
        raise NotImplementedError('Método "make_products_json" não implementado')

    @abstractmethod
    def get_products_data(products_data: dict) -> None:
        raise NotImplementedError('Método "get_products_data" não implementado')
    
    @abstractmethod
    def consult_pagination(page_number: int, total_pages: int) -> None:
        raise NotImplementedError('Método "consult_pagination" não implementado')
    
    @abstractmethod
    def get_consult_endpoint(page_number: int) -> str:
        raise NotImplementedError('Método "get_consult_endpoint" não implementado')

    @abstractmethod
    def get_value_with_discount_prime_ninja(product: dict) -> str:
        raise NotImplementedError('Método "get_value_with_discount_prime_ninja" não implementado')

    @abstractmethod
    def get_value_black_friday(product: dict) -> str:
        raise NotImplementedError('Método "get_value_black_friday" não implementado')

    @abstractmethod
    def get_value_black_friday_with_discount(product: dict) -> str:
        raise NotImplementedError('Método "get_value_black_friday_with_discount" não implementado')