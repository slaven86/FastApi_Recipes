from fastapi import status, APIRouter, HTTPException, Depends
from .database import SessionLocal
from . import models
from passlib.hash import pbkdf2_sha256
from .token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(tags=["Auth"])
db = SessionLocal()

@router.post('/login', status_code=status.HTTP_200_OK)
def login(request: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.User).filter(models.User.username == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    if not pbkdf2_sha256.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invald password!")


    access_token = create_access_token(data={"sub": user.username, "sub2": user.id})
    return {"access_token": access_token, "token_type": "bearer"}