import os
import unittest
from src.logs.logger.Logger import Logger
from src.core.sheets.SheetsCore import SheetsCore
from src.utils.ConvertValues import ConvertValues


class SheetsCoreTest(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.sheets_core = SheetsCore(
            logger=Logger()
        )

    def test_create_xlsx_with_success(self) -> None:
        self.sheets_core.create_xlsx(
            products_list=[{
                "Produto": "Produto Teste",
                "Descrição": "Descrição Teste",
                "Valor Atual": "Valor Teste",
                "Valor com desconto [Prime Ninja]": "Valor com desconto Teste",
                "Valor [Black Friday]": "Valor Black Friday",
                "Valor com desconto [Black Friday]": "Valor Black Friday c/ desconto"
            }
        ])
        self.assertTrue(expr="kabum_produtos.xlsx" in os.listdir())
        os.remove("./kabum_produtos.xlsx")

    if __name__ == "__main__":
        unittest.main()
