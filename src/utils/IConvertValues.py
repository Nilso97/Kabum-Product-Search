from abc import ABC, abstractmethod


class IConvertValues(ABC):

    @staticmethod
    def convert_values(value: str) -> int:
        raise NotImplementedError("Método 'converted_values' não foi implementado corretamente")
    
    @staticmethod
    def convert_datetime(format: str) -> str:
        raise NotImplementedError("Método 'convert_datetime' não foi implementado corretamente")