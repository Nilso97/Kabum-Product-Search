from abc import ABC, abstractmethod


class IRequisitionService(ABC):

    @abstractmethod
    def send_http_client(self, method: str, url: str, body: dict = {}) -> str:
        raise NotImplementedError('Método "send_http_client" não implementado')

    @abstractmethod
    def convert_request_params(self, method: str) -> str:
        raise NotImplementedError('Método "convert_request_params" não implementado')

    @abstractmethod
    def convert_bytes_in_str(self, response: bytes) -> str:
        raise NotImplementedError('Método "convert_bytes_in_str" não implementado')
