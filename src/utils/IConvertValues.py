from abc import ABC, abstractmethod


class IConvertValues(ABC):

    @abstractmethod
    def convert_values(value: str) -> int:
        raise NotImplementedError("Método 'converted_values' não foi implementado corretamente")
    
    @abstractmethod
    def convert_datetime(format: str) -> str:
        raise NotImplementedError("Método 'convert_datetime' não foi implementado corretamente")