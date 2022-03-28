from fastapi import APIRouter, status, HTTPException, Depends
from .schemas import RecipeCreate, UserOut, RecipeList, Ingredient, RateCreate, Rate
from .token import get_current_user
from . import models
from .database import SessionLocal
from typing import List
from sqlalchemy.sql import func, desc


router = APIRouter(tags=['Recipes'])
db = SessionLocal()

@router.post('/recipes', status_code=status.HTTP_201_CREATED)
def add_recipe(recipe: RecipeCreate, current_user: UserOut = Depends(get_current_user)):

    all_names = recipe.ingredients.split()
    ingredient = []
    for name in all_names:
        result = db.query(models.Ingredient).filter(models.Ingredient.name == name).first()
        if result is None:
            ingredient.append(models.Ingredient(name=name))
        else:
            ingredient.append(result)

    new_recipe = models.Recipe(name=recipe.name,
                               description=recipe.description,
                               owner_id=current_user.id,
                               ingredients=ingredient)

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return {"msg": "New recipe created!"}



@router.get('/recipes', status_code=status.HTTP_200_OK, response_model=List[RecipeList])
def get_all_recipes():
    all_recipes = db.query(models.Recipe).all()
    return all_recipes


@router.get('/recipes/{id}', status_code=status.HTTP_200_OK, response_model=RecipeList)
def get_single_recipe(id: int, current_user: UserOut = Depends(get_current_user)):
    single_recipe = db.query(models.Recipe).filter(models.Recipe.id == id,
                                                   models.Recipe.owner_id == current_user.id).first()

    if single_recipe:
        return single_recipe
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Recipe does not exist!")



@router.put('/recipes/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_recipe(id:int, recipe: RecipeCreate, current_user: UserOut = Depends(get_current_user)):

    recipe_update = db.query(models.Recipe).filter(
        models.Recipe.owner_id == current_user.id, models.Recipe.id == id).first()

    if not recipe_update:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only owner can update this page!")

    recipe_update.name = recipe.name
    recipe_update.description = recipe.description
    db.commit()
    return {"msg": "Recipe is updated!"}



@router.delete('/recipes/{id}', status_code=status.HTTP_200_OK)
def delete_recipe(id:int, current_user: UserOut = Depends(get_current_user)):
    recipe_delete = db.query(models.Recipe).filter(
        models.Recipe.owner_id == current_user.id, models.Recipe.id == id).first()

    if not recipe_delete:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only owner can delete this page!")

    db.delete(recipe_delete)
    db.commit()
    return {"msg": "Recipe has been deleted!"}


@router.get('/top-ingredients', status_code=status.HTTP_200_OK, response_model=List[Ingredient])
def get_top_five_ingredients():

    result = db.query(models.Ingredient.name, func.count(models.Ingredient.name))\
        .join(models.RecipeIngredient, models.RecipeIngredient.ingredient_id == models.Ingredient.id)\
        .group_by(models.Ingredient.id).order_by(desc(func.count(models.Ingredient.name))).limit(5).all()

    return result


@router.post('/recipes/rate', status_code=status.HTTP_201_CREATED)
def add_rate(id: int, rating: RateCreate, current_user: UserOut = Depends(get_current_user)):
    if rating.rate not in range(1, 6):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Rate must be 1-5, try again")
    new_rate = models.Rating(recipe_id=id, rate=rating.rate, owner_id=current_user.id)
    query = db.query(models.Recipe).filter(models.Recipe.owner_id == current_user.id,
                                           models.Recipe.id == rating.recipe_id).first()
    if query:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Can not rate your own recipe!")
    db.add(new_rate)
    db.commit()
    db.refresh(new_rate)
    return {"msg": "Your rate added successfully"}



@router.get('/recipes/{id}/rate', status_code=status.HTTP_200_OK,response_model=Rate)
def get_avg_rate(id: int, current_user: UserOut = Depends(get_current_user)):
    single_recipe = db.query(models.Recipe).filter(models.Recipe.id == id,
                                                   models.Recipe.owner_id == current_user.id).first()

    if single_recipe:
        avg = db.query(func.avg(models.Rating.rate)).filter(models.Rating.recipe_id == id).first()
        return Rate(rate=avg[0])
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Recipe does not exist!")

