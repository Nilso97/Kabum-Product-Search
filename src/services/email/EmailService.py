import os
import smtplib
from typing import Type
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from src.logs.logger.ILogger import ILogger
from email.mime.multipart import MIMEMultipart
from src.utils.IConvertValues import IConvertValues
from src.services.email.IEmailService import IEmailService


class EmailService(IEmailService):

    def __init__(
        self, 
        logger: Type[ILogger], 
        convert_values: Type[IConvertValues]
    ) -> None:
        self.logger = logger
        self.convert_values = convert_values
        self.message = MIMEMultipart()
        self.email_address = os.getenv("EMAIL")
        self.smtp = smtplib.SMTP(host="smtp.gmail.com", port=587)
        self.smtp.starttls()

    def send_email(self) -> None:
        try:
            self.logger.message("Enviando e-mail contendo a planilha com os produtos encontrados")
            self.smtp.login(user=str(self.email_address), password=str(os.getenv("PASSWORD")))
            actual_date = self.convert_values.convert_datetime(format="%d/%m/%Y")
            self.make_email_message(email_address=str(self.email_address), actual_date=actual_date)
            self.attach_email_file()
            attached = self.message.as_string()
            self.smtp.sendmail(
                str(self.email_address), 
                str(self.email_address), 
                attached
            )
            self.logger.message(f"E-mail enviado com sucesso para '{self.email_address}'")
        except (Exception) as error:
            error_message = str(error)
            self.logger.error(
                f"Erro ao enviar o e-mail contendo os produtos encontrados: {error_message}")
        finally:
            self.smtp.quit()
            return
        
    def attach_email_file(self) -> None:
        self.logger.message("Anexando arquivo 'kabum_produtos.xlsx' ao e-mail")
        attached_part = MIMEBase("application", "octet-stream")
        attached_part.set_payload(open("./kabum_produtos.xlsx", "rb").read())
        encode_base64(attached_part)
        attached_part.add_header(
            'Content-Disposition',
            "attachament; filename="+"kabum_produtos.xlsx"
        )
        self.message.attach(attached_part)
        
    def make_email_message(self, email_address: str, actual_date: str) -> None:
        email_template = f"""
            <html>
                <body>
                    <p>Olá <strong>{email_address}</strong>,<br> 
                    Segue em anexo a planilha contendo os produtos encontrados no dia {actual_date}:
                    </p>
                </body>
            </html>
        """
        self.message["Subject"] = f"Serviço de Consulta de Preços no site da Kabum - {actual_date}"
        self.message.attach(MIMEText(email_template, "html"))