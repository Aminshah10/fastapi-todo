from fastapi import APIRouter, status, HTTPException, Depends
from app.users.models import UserModel
from app.users.schemas import *
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["users"])

DB_DEPENDENCY = Depends(get_db)

@router.post("/users/login")
def user_login(
    request: LoginUserSchema,
    db: Session = DB_DEPENDENCY
):
    user = (
        db.query(UserModel)
        .filter(UserModel.username == request.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not user.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )

    return user

@router.post("/users/register", status_code=status.HTTP_201_CREATED)
def user_register(
    request: RegisterUserSchema,
    db: Session = DB_DEPENDENCY
):
    user = (
        db.query(UserModel)
        .filter(UserModel.username == request.username)
        .first()
    )

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    if request.password != request.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    new_user = UserModel(
        username=request.username
    )

    new_user.set_password(request.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user