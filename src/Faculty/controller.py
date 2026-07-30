from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.Faculty.dtos import Faculty
from src.Faculty.models import FacultyModel
from src.user.models import UserModel


def create_faculty(body: Faculty, db: Session, user: UserModel) -> FacultyModel:
    new_faculty = FacultyModel(
        Name=body.Name,
        Designation=body.Designation,
        Review=body.Review,
        user_id=user.id,
    )
    db.add(new_faculty)
    db.commit()
    db.refresh(new_faculty)
    return new_faculty


def get_all_faculties(db: Session) -> list[FacultyModel]:
    return db.query(FacultyModel).order_by(FacultyModel.id.desc()).all()


def get_one_faculty(faculty_id: int, db: Session) -> FacultyModel:
    faculty = db.query(FacultyModel).filter(FacultyModel.id == faculty_id).first()
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty not found",
        )
    return faculty


def update_faculty(
    body: Faculty, faculty_id: int, db: Session, user: UserModel
) -> FacultyModel:
    faculty = (
        db.query(FacultyModel)
        .filter(FacultyModel.id == faculty_id, FacultyModel.user_id == user.id)
        .first()
    )

    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty not found or you are not authorized to update it",
        )

    faculty.Name = body.Name
    faculty.Designation = body.Designation
    faculty.Review = body.Review

    db.commit()
    db.refresh(faculty)
    return faculty


def delete_faculty(faculty_id: int, db: Session, user: UserModel) -> None:
    faculty = (
        db.query(FacultyModel)
        .filter(FacultyModel.id == faculty_id, FacultyModel.user_id == user.id)
        .first()
    )

    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty not found or you are not authorized to delete it",
        )

    db.delete(faculty)
    db.commit()
