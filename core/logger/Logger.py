import logging


class Logger():

    def __init__(self) -> None:
        self.get_basic_config()

    def get_basic_config(self):
        date_format = '%d/%m/%Y %I:%M:%S'
        message_format = '%(levelname)s - %(asctime)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO, format=message_format, datefmt=date_format)

    def send_info_message(self, message: str):
        return logging.info(msg=message)

    def send_error_message(self, message: str):
        return logging.error(msg=message)

    def send_alert_message(self, message: str):
        return logging.warning(msg=message)
