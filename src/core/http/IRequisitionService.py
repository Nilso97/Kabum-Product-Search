import http.client
from abc import ABC, abstractmethod


class IRequisitionService(ABC):

    @abstractmethod
    def send_http_client(self, method: str, url: str, body: dict = {}) -> str:
        raise NotImplementedError("Método 'send_http_client' não foi implementado corretamente")

    @abstractmethod
    def convert_request_params(self, method: str) -> str:
        raise NotImplementedError("Método 'convert_request_params' não foi implementado corretamente")

    @abstractmethod
    def convert_response_data(self, response: http.client.HTTPResponse) -> str:
        raise NotImplementedError("Método 'convert_response_data' não foi implementado corretamente")
