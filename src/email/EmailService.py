import os
import smtplib
from typing import Type
from datetime import datetime
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from src.logs.logger.ILogger import ILogger
from email.mime.multipart import MIMEMultipart
from src.email.IEmailService import IEmailService


class EmailService(IEmailService):

    def __init__(self, logger: Type[ILogger]) -> None:
        self.logger = logger
        self.message = MIMEMultipart()
        self.__email_address = os.getenv("EMAIL")
        self.__email_password = os.getenv("PASSWORD")
        self.smtp = smtplib.SMTP(host="smtp.gmail.com", port=587)
        self.smtp.starttls()

    def send_email(self) -> None:
        try:
            self.smtp.login(str(self.__email_address), str(self.__email_password))
            self.make_email_message(str(self.__email_address), datetime.now().strftime("%d/%m/%Y"))
            self.attach_email_file()
            attached = self.message.as_string()
            self.smtp.sendmail(
                str(self.__email_address), 
                str(self.__email_address), 
                attached
            )
            self.logger.message(f"E-mail enviado com sucesso para o endereço '{self.__email_address}'")
        except (Exception) as error:
            error_message = str(error)
            self.logger.error(f"Erro ao enviar o e-mail contendo os produtos encontrados: {error_message}")
        finally:
            self.smtp.quit()
        
    def attach_email_file(self) -> None:
        attached_part = MIMEBase("application", "octet-stream")
        attached_part.set_payload(open("./kabum_produtos.xlsx", "rb").read())
        encode_base64(attached_part)
        attached_part.add_header(
            "Content-Disposition",
            "attachament; filename="+"kabum_produtos.xlsx"
        )
        self.message.attach(attached_part)
        
    def make_email_message(self, email_address: str, actual_date: str) -> None:
        self.message["Subject"] = f"Serviço de Consulta de Preços no site da Kabum - {actual_date}"
        email_template = """
            <html>
                <body>
                    <p>Olá <strong>{}</strong>,<br> 
                    Segue em anexo a planilha contendo os produtos encontrados no dia {}:
                    </p>
                </body>
            </html>
        """
        self.message.attach(MIMEText(email_template.format(email_address, actual_date), "html"))