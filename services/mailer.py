import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib
from email import encoders


class Mailer:

    def __init__(self, server, email_sender, password):
        self.email_sender = email_sender
        self.password = password
        self.server = smtplib.SMTP(server, 587)
        self.server.starttls()

    def send_mail(self, email_recipient, message, path_to_file):
        subject = 'Тестовое задание от "Гринатом"'
        msg = MIMEMultipart()
        msg["Subject"] = subject            # тема письма
        msg["From"] = self.email_sender
        msg["To"] = email_recipient
        # добавляем в письмо текст сообщения
        msg.attach(MIMEText(message, "plain"))

        # Добавляем возможность прикрепить файл любого типа
        file_path = path_to_file
        basename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        file_attachment = MIMEBase("application", f"octet-stream; name={basename}")

        with open(file_path, "rb") as f:
            file_bytes = f.read()

        file_attachment.set_payload(file_bytes)
        file_attachment.add_header("Content-Description", f"attachment; filename={basename}; size={file_size}")
        encoders.encode_base64(file_attachment)
        # прикрепляем файл
        msg.attach(file_attachment)

        try:
            self.server.login(self.email_sender, self.password)
            self.server.sendmail(self.email_sender, email_recipient, msg.as_string())
            self.server.quit()
            return "Письмо успешно отправлено!"

        except Exception as ex:
            return f"{ex}\n Проверьте логин и пароль."




