from abc import ABC, abstractmethod


class ISheetsCore(ABC):

    @abstractmethod
    def create_xlsx(products_list: list[dict]) -> None:
        raise NotImplementedError("Método 'create_xlsx' não foi implementado corretamente")

    @abstractmethod
    def create_xlsx_headers() -> None:
        raise NotImplementedError("Método 'create_xlsx_headers' não foi implementado corretamente")
