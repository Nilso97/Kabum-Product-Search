from abc import ABC, abstractmethod


class ILogger(ABC):

    @abstractmethod
    def set_basic_config_init(self):
        raise NotImplementedError("Método 'basic_config_init' não foi implementado corretamente")

    @abstractmethod
    def message(self, message: str):
        raise NotImplementedError("Método 'message' não foi implementado corretamente")

    @abstractmethod
    def error(self, message: str):
        raise NotImplementedError("Método 'error' não foi implementado corretamente")

    @abstractmethod
    def alert(self, message: str):
        raise NotImplementedError("Método 'alert' não foi implementado corretamente")
