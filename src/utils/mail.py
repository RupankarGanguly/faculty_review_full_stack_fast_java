from typing import List

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel


class EmailSchema(BaseModel):
    email: List[EmailStr]


# NOTE: For production move these to .env
conf = ConnectionConfig(
    MAIL_USERNAME="rupankarganguly492@gmail.com",
    MAIL_PASSWORD="eztw vnia tdwf kozd",
    MAIL_FROM="rupankarganguly492@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="Faculty Review System",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_email(email: List[str]) -> dict:
    html = """
    <h2>Welcome!</h2>
    <p>Hi, thanks for registering on the Faculty Review Management System.</p>
    <p>You can now log in and start adding faculty reviews.</p>
    """

    message = MessageSchema(
        subject="Registration Successful – Faculty Review System",
        recipients=email,
        body=html,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message": "email has been sent"}
