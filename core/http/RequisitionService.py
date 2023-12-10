import http.client
from logs.logger.Logger import Logger
from core.http.IRequisitionService import IRequisitionService


class RequisitionService(IRequisitionService):

    def __init__(self) -> None:
        self.logger = Logger()
        self.conn = http.client.HTTPSConnection(host='kabum.com.br', port=443)
        
    def send_http_client(self, method: str, url: str, body: dict = {}) -> str:
        """"""
        try:
            request_method = self.convert_request_params(method=method)
            default_user_agent = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' +
                '(KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
            }
            if request_method == 'GET':
                self.conn.request(
                    method=request_method,
                    url=url,
                    headers=default_user_agent
                )
            elif request_method == 'POST':
                self.conn.request(
                    method=request_method,
                    url=url,
                    headers=default_user_agent,
                    body=body
                )
            # TODO adicionar os demais métodos HTTP (caso necessário)
            response = self.conn.getresponse()

            if response.status != 200 or not response:
                raise Exception('O site "kabum.com.br" está fora do ar!')

            converted_response = self.convert_bytes_in_str(response=response)
        except (Exception) as error:
            converted_response = str(error)
            self.logger.error(f'Erro na função "send_http_client()" -> {converted_response}')
        finally:
            return converted_response

    def convert_request_params(self, method: str) -> str:
        """"""
        return method.upper() if method.lower() else method

    def convert_bytes_in_str(self, response: bytes) -> str:
        """"""
        return response.read().decode('utf-8')
