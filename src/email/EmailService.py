import os
import smtplib
from datetime import datetime
from dotenv import load_dotenv
from src.logs.logger.Logger import Logger
from src.email.IEmailService import IEmailService


class EmailService(IEmailService):

    def __init__(self) -> None:
        self.logger = Logger()
        self.smtp = smtplib.SMTP(host="smtp.gmail.com", port=587)
        load_dotenv(dotenv_path="./.env")
        self.smtp.starttls()

    def send_email(self) -> None:
        try:
            email_address = os.getenv("EMAIL")
            actual_date = datetime.now().strftime("%d/%m/%Y")
            hour = datetime.now().strftime("%H:%M:%S")
            self.logger.information(
                "Enviando e-mail contendo a planilha com os produtos encontrados\n\nAguarde...")
            mail_message = "Olá, segue em anexo a planilha contendo os produtos encontrados"
            mail_message += f"no dia {actual_date} às {hour}"
            self.smtp.login(user=email_address, password=os.getenv("PASSWORD"))
            self.smtp.sendmail(
                msg=mail_message.encode("utf-8"),
                from_addr=email_address,
                to_addrs=email_address
            )
            self.logger.information(f"E-mail enviado com sucesso para o endereço '{email_address}'")
        except (Exception) as error:
            self.logger.error(
                f"Erro ao enviar o e-mail contendo os produtos encontrados: {error}")
        finally:
            self.smtp.quit()
