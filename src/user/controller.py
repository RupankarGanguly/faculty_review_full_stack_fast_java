from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status, BackgroundTasks
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from src.user.dtos import UserSchema, UserLoginSchema
from src.user.models import UserModel
from src.utils.settings import settings
from src.utils.mail import send_email

password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


async def registration(
    body: UserSchema, db: Session, bg_tasks: BackgroundTasks
) -> UserModel:
    if db.query(UserModel).filter(UserModel.username == body.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    if db.query(UserModel).filter(UserModel.email == body.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    new_user = UserModel(
        name=body.name,
        username=body.username,
        hash_password=get_password_hash(body.password),
        email=body.email,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Send welcome email in background (won't block response)
    try:
        bg_tasks.add_task(send_email, [new_user.email])
    except Exception:
        pass  # email failure should not break registration

    return new_user


def login_user(body: UserLoginSchema, db: Session) -> dict:
    user = db.query(UserModel).filter(UserModel.username == body.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if not password_hash.verify(body.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.EXP_TIME)

    token = jwt.encode(
        {
            "username": user.username,
            "id": user.id,
            "exp": exp,
        },
        settings.Secret_key,
        algorithm=settings.Algorithm,
    )

    return {"token": token, "username": user.username, "name": user.name}
