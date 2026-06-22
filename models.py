from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


# SQLAlchemy model (database table)
class Lead(Base):

    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    company = Column(String)
    email = email = Column(String, unique=True)
    user_id = Column(
        Integer, 
        ForeignKey("users.id")
    )


# Pydantic model (API input validation)
class LeadCreate(BaseModel):
    name: str
    company: str
    email: str
class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(
        String,
        unique=True
    )

    password = Column(String)

    role = Column(
        String,
        default="user"
    )


class UserCreate(BaseModel):

    email: str
    password: str
    role: str = "user"