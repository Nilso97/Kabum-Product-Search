import logging
from src.logs.logger.ILogger import ILogger


class Logger(ILogger):

    def __init__(self) -> None:
        self._basic_config()

    @staticmethod
    def _basic_config() -> None:
        message_format = '%(levelname)s - %(asctime)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=message_format, datefmt="%d/%m/%Y %H:%M:%S")

    @staticmethod
    def message(message: str) -> None:
        logging.info(f"KABUM - Consulta de Preços - {message}")

    @staticmethod
    def error(message: str) -> None:
        logging.error(f"KABUM - Consulta de Preços - {message}")

    @staticmethod
    def alert(message: str) -> None:
        logging.warning(f"KABUM - Consulta de Preços - {message}")
