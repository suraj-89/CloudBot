from fastapi import APIRouter
from models import User, UserCreate
from database import SessionLocal
from auth import hash_password
from sqlalchemy.exc import IntegrityError

router = APIRouter()


@router.post("/signup")
def signup(user: UserCreate):

    db = SessionLocal()

    try:

        hashed_password = hash_password(
            user.password
        )

        new_user = User(
    email=user.email,
    password=hashed_password,
    role=user.role
)

        db.add(new_user)

        db.commit()

        return {
            "message":"User created successfully"
        }

    except IntegrityError:

        db.rollback()

        return {
            "message":"Email already exists"
        }
    

from auth import verify_password
from jwt_handler import create_access_token


@router.post("/login")
def login(user: UserCreate):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:

        return {
            "message": "Invalid email"
        }

    if not verify_password(
        user.password,
        existing_user.password
    ):

        return {
            "message": "Wrong password"
        }

    token = create_access_token(
        {
            "email": existing_user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }