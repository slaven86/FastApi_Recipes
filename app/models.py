from .database import Base
from sqlalchemy import Column, Text, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100))
    username = Column(String(50))
    password = Column(String(200))

    my_recipes = relationship("Recipe", back_populates="owner")
    recipes = relationship("Recipe", secondary="rating", back_populates="owners")



class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id",  ondelete="CASCADE"))

    owner = relationship("User", back_populates="my_recipes")
    ingredients = relationship('Ingredient', secondary="recipe_ingredient", back_populates='recipes')
    owners = relationship("User", secondary="rating", back_populates="recipes")




class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    recipes = relationship('Recipe', secondary="recipe_ingredient", back_populates='ingredients')


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredient"

    recipe_id = Column(Integer, ForeignKey('recipes.id',  ondelete="CASCADE"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id',  ondelete="CASCADE"), primary_key=True)



class Rating(Base):
    __tablename__ = "rating"

    recipe_id = Column(Integer, ForeignKey('recipes.id',  ondelete="CASCADE"), primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id',  ondelete="CASCADE"), primary_key=True)
    rate = Column(Float)
