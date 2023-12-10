import logging
from logs.logger.ILogger import ILogger


class Logger(ILogger):

    def __init__(self) -> None:
        self.basic_config_init()

    def basic_config_init(self):
        message_format = '%(levelname)s - %(asctime)s - %(message)s'
        logging.basicConfig(level=logging.INFO,format=message_format, datefmt='%d/%m/%Y %I:%M:%S')

    def information(self, message: str) -> None:
        logging.info(f'KABUM - Consulta de preços - {message}')

    def error(self, message: str) -> None:
        logging.error(f'KABUM - Consulta de preços - {message}')

    def alert(self, message: str) -> None:
        logging.warning(f'KABUM - Consulta de preços - {message}')
