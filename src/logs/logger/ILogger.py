from abc import ABC, abstractmethod


class ILogger(ABC):

    @staticmethod
    def __basic_config() -> None:
        raise NotImplementedError("Método 'basic_config' não foi implementado corretamente")

    @staticmethod
    def message(message: str) -> None:
        raise NotImplementedError("Método 'message' não foi implementado corretamente")

    @staticmethod
    def error(message: str) -> None:
        raise NotImplementedError("Método 'error' não foi implementado corretamente")

    @staticmethod
    def alert(message: str) -> None:
        raise NotImplementedError("Método 'alert' não foi implementado corretamente")
