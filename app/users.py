from fastapi import APIRouter, status, HTTPException, Depends
from .database import SessionLocal
from .schemas import UserCreate, UserOut, RecipeList
from . import models
import validators
from passlib.hash import pbkdf2_sha256
from typing import List
from .token import get_current_user

router = APIRouter(tags=['Users'])
db = SessionLocal()


@router.post('/users', status_code=status.HTTP_201_CREATED)
def add_user(user: UserCreate):
    if len(user.first_name) < 2:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="First name must be min 2 characters!")

    if not user.first_name.isalpha():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="First name must be only letters!")

    if len(user.last_name) < 2:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Last name must be min 2 characters!")

    if not user.last_name.isalpha() or " " in user.last_name:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Last name must be only letters!")

    if not validators.email(user.email):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Not valid email!")

    if db.query(models.User).filter(models.User.email == user.email).first() is not None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email already exist!")

    if not user.username.isalnum() or " " in user.username:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Username must be alphanumeric, also no spaces!")
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Username already exist!")

    if len(user.password) < 6:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Password must be min 6 characters!")

    hashed_pass = pbkdf2_sha256.hash(user.password)
    new_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        username=user.username,
        password=hashed_pass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "New user created!"}

@router.get('/users', response_model=List[UserOut], status_code=status.HTTP_200_OK)
def get_all_users():
    all_users = db.query(models.User).all()
    return all_users


@router.get('/users/{id}/recipes', status_code=status.HTTP_200_OK, response_model=List[RecipeList])
def get_own_recipes(id: int, current_user: UserOut = Depends(get_current_user)):
    single_user = db.query(models.User).get(id)
    all_my_recipes = single_user.my_recipes
    user = db.query(models.User).filter(models.User.id == current_user.id).first()

    if single_user == user:
        return all_my_recipes
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only owner can see this page!")


