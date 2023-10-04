from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

import os
from src.config import *


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

config = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_FROM=MAIL_FROM,
    MAIL_FROM_NAME=MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    TEMPLATE_FOLDER=os.path.join(BASE_DIR, 'frontend/public/email')
)


async def async_send_mail(subject: str, email_to: str, body: dict, template: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype='html'
    )

    mail = FastMail(config)
    await mail.send_message(message, template_name=template)

