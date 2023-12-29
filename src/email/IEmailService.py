from abc import ABC, abstractmethod


class IEmailService(ABC):

    @abstractmethod
    def send_email() -> None:
        raise NotImplementedError("Método 'send_email' não foi implementado corretamente")
