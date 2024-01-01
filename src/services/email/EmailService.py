import os
import smtplib
from typing import Type
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from src.logs.logger.ILogger import ILogger
from email.mime.multipart import MIMEMultipart
from src.services.email.IEmailService import IEmailService
from src.utils.IConvertValues import IConvertValues


class EmailService(IEmailService):

    def __init__(
        self, 
        logger: Type[ILogger], 
        convert_values: Type[IConvertValues]
    ) -> None:
        self.logger = logger
        self.convert_values = convert_values
        self.message = MIMEMultipart()
        self.smtp = smtplib.SMTP(host="smtp.gmail.com", port=587)
        self.smtp.starttls()

    def send_email(self) -> None:
        try:
            email_address = os.getenv("EMAIL")
            self.logger.information(
                "Enviando e-mail contendo a planilha com os produtos encontrados\n\nAguarde...")
            actual_date = self.convert_values.convert_datetime(format="%d/%m/%Y")
            self.smtp.login(user=email_address, password=os.getenv("PASSWORD"))
            self.make_email_message(email_address=email_address, actual_date=actual_date)
            self.attach_email_file()
            attached = self.message.as_string()
            self.smtp.sendmail(
                email_address, 
                email_address, 
                attached
            )
            self.logger.information(f"E-mail enviado com sucesso para o endereço '{email_address}'")
        except (Exception) as error:
            self.logger.error(
                f"Erro ao enviar o e-mail contendo os produtos encontrados: {error}")
            self.smtp.quit()
        finally:
            self.smtp.quit()
            return
        
    def attach_email_file(self) -> None:
        mail_part = MIMEBase("application", "octet-stream")
        mail_part.set_payload(open("./kabum_produtos.xlsx", "rb").read())
        encode_base64(mail_part)
        mail_part.add_header(
            'Content-Disposition',
            "attachament; filename="+"kabum_produtos.xlsx"
        )
        self.message.attach(mail_part)
        
    def make_email_message(
        self, 
        email_address: str, 
        actual_date: str
    ) -> None:
        email_message = f"Olá {email_address},\n\n"
        email_message += f"Segue em anexo a planilha contendo os produtos encontrados no dia {actual_date}:"
        self.message['Subject'] = f"Serviço de Consulta de Preços no site da Kabum - {actual_date}"
        self.message.attach(MIMEText(email_message, "plain"))