from abc import ABC, abstractmethod


class ISheetsCore(ABC):

    @abstractmethod
    def create_xlsx(self, products_list: list[dict]) -> None:
        raise NotImplementedError("Método 'create_xlsx' não foi implementado corretamente")

    @abstractmethod
    def create_xlsx_headers(self) -> None:
        raise NotImplementedError("Método 'create_xlsx_headers' não foi implementado corretamente")
