import logging


class LoggerService():

    def __init__(self) -> None:
        self.basic_config_init()

    def basic_config_init(self):
        date_format = '%d/%m/%Y %I:%M:%S'
        msg_format = '%(levelname)s - %(asctime)s - %(message)s'
        logging.basicConfig(level=logging.INFO,format=msg_format, datefmt=date_format)

    def send_info_msg(self, message: str):
        return logging.info(msg=message)

    def send_error_msg(self, message: str):
        return logging.error(msg=message)

    def send_alert_msg(self, message: str):
        return logging.warning(msg=message)
