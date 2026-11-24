from pydantic import BaseModel, Field
from typing import List

class InventoryResponse(BaseModel):
    usable_items: List[str]
    message: str

class DietResponse(BaseModel):
    compatible_items: List[str]
    suggested_recipe_ideas: List[str]

class InventoryInput(BaseModel):
    items: List[str]

class DietInput(BaseModel):
    items: List[str]
    diet: str

class AskInput(BaseModel):
    items: List[str]
    diet: str

class AskResponse(BaseModel):
    usable_items: List[str]
    diet_filtered: List[str]
    suggestions: List[str]

class RecipeStep(BaseModel):
    step_number: int
    instruction: str

class RecipeResponse(BaseModel):
    title: str
    ingredients: List[str]
    steps: List[RecipeStep]

class PlanInput(BaseModel):
    base_recipe: str

class RecommendInput(BaseModel):
    items: List[str]
    diet: str
    recipe_count: int = Field(default=5, ge=1, le=5)

class RecommendResponse(BaseModel):
    recipes: List[RecipeResponse]