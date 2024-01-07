from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from backend.config import *


BASE_DIR = os.path.dirname(__file__)

config = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_FROM=MAIL_FROM,
    MAIL_FROM_NAME=MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    TEMPLATE_FOLDER=os.path.join(BASE_DIR, 'email_templates')
)


async def async_send_mail(subject: str, email_to: str, body: dict, template: str):
    """Send an email to a user"""
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype='html'
    )

    mail = FastMail(config)
    await mail.send_message(message, template_name=template)

