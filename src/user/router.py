from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session

from src.user.dtos import UserLoginSchema, UserSchema, UserResponseSchema
from src.utils.db import get_db
from src.user import controller

user_routes = APIRouter(prefix="/user", tags=["User"])


@user_routes.post(
    "/register",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    body: UserSchema,
    bg_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    return await controller.registration(body, db, bg_tasks)


@user_routes.post("/login", status_code=status.HTTP_200_OK)
def login_user(body: UserLoginSchema, db: Session = Depends(get_db)):
    return controller.login_user(body, db)
