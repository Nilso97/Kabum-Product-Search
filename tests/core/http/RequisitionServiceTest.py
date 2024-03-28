import unittest
from src.logs.logger.Logger import Logger
from src.infra.http.RequisitionService import RequisitionService


class RequisitionServiceTest(unittest.TestCase):
    
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.http_request = RequisitionService(logger=Logger())
        
    def test_send_http_request_with_success(self) -> None:
        site_response = self.http_request.send_http_client(
            method="get",
            url="https://www.kabum.com.br"
        )
        self.assertIsNotNone(obj=site_response)
        self.assertEqual(
            first=type(site_response),
            second=str,
        )
        
    if __name__ == "__main__":
        unittest.main()