import os
import time
import unittest
from src.logs.logger.Logger import Logger
from src.core.sheets.SheetsCore import SheetsCore
from src.utils.ConvertValues import ConvertValues


class SheetsCoreTest(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.xlsx = SheetsCore(logger=Logger(), convert_values=ConvertValues())

    def test_create_xlsx(self) -> None:
        self.xlsx.create_xlsx(
            products_list=[{
                "Produto": "teste",
                "Descrição": "teste",
                "Valor Atual": "teste",
                "Valor com desconto [Prime Ninja]": "teste",
                "Valor [Black Friday]": "teste",
                "Valor com desconto [Black Friday]": "teste"
            }
        ])
        self.assertTrue(expr="kabum_produtos.xlsx" in os.listdir())
        time.sleep(1)
        os.remove("./kabum_produtos.xlsx")

    if __name__ == "__main__":
        unittest.main()
