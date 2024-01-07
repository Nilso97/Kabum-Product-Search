from abc import ABC, abstractmethod


class IEmailService(ABC):

    @abstractmethod
    def send_email(self) -> None:
        raise NotImplementedError("Método 'send_email' não foi implementado corretamente")

    @abstractmethod
    def attach_email_file(self) -> None:
        raise NotImplementedError("Método 'attach_email_file' não foi implementado corretamente")

    @abstractmethod
    def make_email_message(self, email_address: str, actual_date: str) -> None:
        raise NotImplementedError("Método 'make_email_message' não foi implementado corretamente")
