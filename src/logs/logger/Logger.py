import logging
from src.logs.logger.ILogger import ILogger


class Logger(ILogger):
    
    def __init__(self) -> None:
        self.basic_config()

    @staticmethod
    def basic_config() -> None:
        message_format = '%(levelname)s - %(asctime)s - %(message)s'
        logging.basicConfig(level=logging.INFO,format=message_format, datefmt="%d/%m/%Y %I:%M:%S")

    @staticmethod
    def message(message: str) -> None:
        logging.info(f"KABUM - Consulta de Produtos - {message}")

    @staticmethod
    def error(message: str) -> None:
        logging.error(f"KABUM - Consulta de Produtos - {message}")
    
    @staticmethod
    def alert(message: str) -> None:
        logging.warning(f"KABUM - Consulta de Produtos - {message}")
