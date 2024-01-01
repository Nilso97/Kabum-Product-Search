import logging
from src.logs.logger.ILogger import ILogger


class Logger(ILogger):

    def __init__(self) -> None:
        self.set_basic_config_init()

    def set_basic_config_init(self):
        message_format = '%(levelname)s - %(asctime)s - %(message)s'
        logging.basicConfig(level=logging.INFO,format=message_format, datefmt="%d/%m/%Y %I:%M:%S")

    def message(self, message: str) -> None:
        logging.info(f"KABUM - Consulta de Produtos - {message}")

    def error(self, message: str) -> None:
        logging.error(f"KABUM - Consulta de Produtos - {message}")

    def alert(self, message: str) -> None:
        logging.warning(f"KABUM - Consulta de Produtos - {message}")
