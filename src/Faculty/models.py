from sqlalchemy import Column, Integer, String, ForeignKey

from src.utils.db import Base


class FacultyModel(Base):
    __tablename__ = "faculty_table"

    id = Column(Integer, primary_key=True, index=True)
    Name = Column(String, nullable=False)
    Designation = Column(String, nullable=False)
    Review = Column(String, nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("Faculty_user_table.id", ondelete="CASCADE"),
        nullable=False,
    )
