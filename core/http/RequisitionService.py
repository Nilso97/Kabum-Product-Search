import http.client
from core.http.IRequisitionService import IRequisitionService
from core.logger.Logger import Logger


class RequisitionService(IRequisitionService):

    def __init__(self) -> None:
        self.conn = http.client.HTTPSConnection(host='kabum.com.br', port=443)
        self.logger = Logger()

    def send_http_client(self, method: str, url: str, body: dict = {}):
        """"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' +
                '(KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
            }
            if method == 'get':
                self.conn.request(
                    method='GET',
                    url=url,
                    headers=headers
                )
            elif method == 'post':
                self.conn.request(
                    method='POST',
                    url=url,
                    headers=headers,
                    body=body
                )
            response = self.conn.getresponse()

            if response.status != 200 or not response:
                raise Exception('O site "kabum.com.br" está fora do ar!')

            final_response = self.convert_bytes_in_str(response=response)
        except (Exception) as error:
            final_response = error
            self.logger.send_error_message(
                'Erro na função "send_http_client()" ->', str(error))
        finally:
            return final_response

    def convert_bytes_in_str(self, response: bytes) -> str:
        """"""
        return response.read().decode('utf-8')
