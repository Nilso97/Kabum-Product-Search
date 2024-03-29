import http.client
from typing import Type
from src.logs.logger.ILogger import ILogger
from src.infra.http.IRequisitionService import IRequisitionService


class RequisitionService(IRequisitionService):

    def __init__(self, logger: Type[ILogger]) -> None:
        self.logger = logger
        self.http_client = http.client.HTTPSConnection(
            host='kabum.com.br', 
            port=443, 
            timeout=2*60
        )
        
    def send_http_client(self, method: str, url: str, body: dict = {}) -> str:
        request_method = self.convert_request_params(method=method)
        try:
            default_headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' +
                '(KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
            }
            if request_method == 'GET':
                self.http_client.request(
                    method=request_method,
                    url=url,
                    headers=default_headers
                )
            elif request_method == 'POST':
                self.http_client.request(
                    method=request_method,
                    url=url,
                    headers=default_headers,
                    body=body
                )

            # TODO adicionar os demais métodos HTTP (caso necessário)

            site_response = self.http_client.getresponse()
            if not site_response or (site_response.status != 200):
                raise Exception('O site "kabum.com.br" está fora do ar!')

            converted_response = self.convert_response_data(response=site_response)
        except (Exception) as error:
            converted_response = str(error)
            self.logger.error(f"Erro ao realizar a requisição HTTP: {converted_response}")
        finally:
            return converted_response

    @staticmethod
    def convert_request_params(method: str) -> str:
        return method.upper() if method.lower() else method

    @staticmethod
    def convert_response_data(response: http.client.HTTPResponse) -> str:
        return response.read().decode('utf-8')
    