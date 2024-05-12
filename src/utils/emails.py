from fastapi.responses import JSONResponse
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from utils.settings import getSettings


settings = getSettings()
conf = ConnectionConfig(
    MAIL_USERNAME = settings.ADMIN_EMAIL_USERNAME,
    MAIL_PASSWORD = settings.ADMIN_EMAIL_PASSWORD,
    MAIL_FROM = settings.ADMIN_EMAIL,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)
fm = FastMail(conf)


async def send_verify_message(email: EmailStr, token: str) -> JSONResponse:
    message = MessageSchema(
        subject="Thanks for using TASKraken",
        recipients=[email],
        body=f"To confirm your enter this token to request in uoyr client. DO NOT do it, if you have not registered this email. Let us know by replying to this email\nyour token: {token}",
        subtype=MessageType.plain
    )
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
