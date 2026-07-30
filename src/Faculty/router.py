from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.Faculty import controller
from src.Faculty.dtos import Faculty, FacultyResponseSchema
from src.utils.db import get_db
from src.utils.helper import is_authenticated
from src.user.models import UserModel

facultyrouter = APIRouter(prefix="/task", tags=["Faculty"])


@facultyrouter.post(
    "/create",
    response_model=FacultyResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    body: Faculty,
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated),
):
    return controller.create_faculty(body, db, user)


@facultyrouter.get(
    "/get_all",
    response_model=List[FacultyResponseSchema],
    status_code=status.HTTP_200_OK,
)
def get_all_tasks(
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated),
):
    return controller.get_all_faculties(db)


@facultyrouter.get(
    "/one_task/{faculty_id}",
    response_model=FacultyResponseSchema,
    status_code=status.HTTP_200_OK,
)
def get_one_task(
    faculty_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated),
):
    return controller.get_one_faculty(faculty_id, db)


@facultyrouter.put(
    "/update/{faculty_id}",
    response_model=FacultyResponseSchema,
    status_code=status.HTTP_200_OK,
)
def update_task(
    body: Faculty,
    faculty_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated),
):
    return controller.update_faculty(body, faculty_id, db, user)


@facultyrouter.delete(
    "/delete/{faculty_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    faculty_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated),
):
    controller.delete_faculty(faculty_id, db, user)
    return None
