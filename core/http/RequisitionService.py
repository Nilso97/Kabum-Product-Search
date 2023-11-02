import http.client
from core.http.IRequisitionService import IRequisitionService


class RequisitionService(IRequisitionService):

    def __init__(self) -> None:
        self.conn = http.client.HTTPSConnection(host='kabum.com.br', port=443)

    def send_http_client(self, method: str, url: str):
        try:
            self.conn.request(
                method=method,
                url=url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
                }
            )
            response = self.convert_bytes_in_str(
                response=self.conn.getresponse())
        except (Exception) as error:
            response = error
            print('Erro na função "send_http_client()" ->', str(error))
        finally:
            return response

    def convert_bytes_in_str(self, response: bytes) -> str:
        return response.read().decode('utf-8')
