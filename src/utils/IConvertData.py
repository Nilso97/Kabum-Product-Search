from abc import ABC, abstractmethod


class IConvertData(ABC):

    @abstractmethod
    def converted_values(value: str) -> int:
        raise NotImplementedError("Método 'converted_values' não foi implementado corretamente")