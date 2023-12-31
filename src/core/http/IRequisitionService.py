from abc import ABC, abstractmethod


class IRequisitionService(ABC):

    @abstractmethod
    def send_http_client(method: str, url: str, body: dict = {}) -> str:
        raise NotImplementedError("Método 'send_http_client' não foi implementado corretamente")

    @abstractmethod
    def convert_request_params(method: str) -> str:
        raise NotImplementedError("Método 'convert_request_params' não foi implementado corretamente")

    @abstractmethod
    def convert_bytes_in_str(response: bytes) -> str:
        raise NotImplementedError("Método 'convert_bytes_in_str' não foi implementado corretamente")
