import xlsxwriter
from typing import Type
from src.logs.logger.ILogger import ILogger
from src.core.sheets.ISheetsCore import ISheetsCore


class SheetsCore(ISheetsCore):

    def __init__(self, logger: Type[ILogger]) -> None:
        self.logger = logger
        self.xlsx = xlsxwriter.Workbook(filename="./kabum_produtos.xlsx")
        self.work_sheet = self.xlsx.add_worksheet()

    def create_xlsx(self, products_list: list[dict]) -> None:
        try:
            self.logger.message("Montando o arquivo '.xlsx' que contém todos os produtos encontrados")
            self.create_xlsx_headers()

            for row, product in enumerate(products_list, 2):
                self.work_sheet.write("A" + str(row), product.get("Produto"))
                self.work_sheet.write("B" + str(row), product.get("Descricao"))
                self.work_sheet.write("C" + str(row), product.get("Valor atual"))
                self.work_sheet.write("D" + str(row), product.get("Valor [Black Friday]"))
                self.work_sheet.write("E" + str(row), product.get("Valor com desconto [Prime Ninja]"))
                self.work_sheet.write("F" + str(row), product.get("Valor com desconto [Black Friday]"))

            self.logger.message("Arquivo 'kabum_produtos.xlsx' criado com sucesso!")
        except (Exception) as error:
            self.logger.error(f"Erro ao montar o arquivo '.xlsx' contendo os produtos encontrados - {error}")
        finally:
            self.xlsx.close()

    def create_xlsx_headers(self) -> None:
        header_format = self.xlsx.add_format({
            "bold": True,
            "bg_color": "#f95d00"
        })
        self.work_sheet.set_row(0, None, header_format)
        self.work_sheet.write("A1", "Produto")
        self.work_sheet.write("B1", "Descrição")
        self.work_sheet.write("C1", "Valor Atual")
        self.work_sheet.write("D1", "Valor [Prime Ninja]")
        self.work_sheet.write("E1", "Valor [Black Friday]")
        self.work_sheet.write("F1", "Valor [Black Friday c/ desconto]")
