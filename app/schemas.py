from pydantic import BaseModel
from typing import Optional, List



class User(BaseModel):
    username: str

    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    first_name: str
    username: str

    class Config:
        orm_mode = True


class Ingredient(BaseModel):
    name: str


    class Config:
        orm_mode = True





class RecipeCreate(BaseModel):
    name: str
    description: str
    ingredients: str

    class Config:
        orm_mode = True




class RecipeList(BaseModel):
    id: int
    name: str
    description: str
    owner: User
    ingredients: List[Ingredient]


    class Config:
        orm_mode = True



class Rate(BaseModel):
    rate: float

    class Config:
        orm_mode = True



class RateCreate(BaseModel):
    recipe_id: int
    rate: float

    class Config:
        orm_mode = True





class TokenData(BaseModel):
    username: Optional[str] = None
    id: Optional[int] = None

