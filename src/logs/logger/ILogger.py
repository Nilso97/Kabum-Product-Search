from abc import ABC, abstractmethod


class ILogger(ABC):

    @abstractmethod
    def basic_config_init(self):
        raise NotImplementedError('Método "basic_config_init" não foi implementado corretamente')

    @abstractmethod
    def information(self, message: str):
        raise NotImplementedError('Método "basic_config_init" não foi implementado corretamente')

    @abstractmethod
    def error(self, message: str):
        raise NotImplementedError('Método "basic_config_init" não foi implementado corretamente')

    @abstractmethod
    def alert(self, message: str):
        raise NotImplementedError('Método "basic_config_init" não foi implementado corretamente')
