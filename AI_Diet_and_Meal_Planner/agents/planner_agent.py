from models import RecipeResponse
from services.llm_client import LLMClient

class PlannerAgent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, base_recipe: str) -> RecipeResponse:
        prompt = (
            f"You are a professional cook. Given the JSON base recipe:\n"
            f"{base_recipe}\n"
            "Rules: \n"
            "1. Analyze the name of the recipe carefully\n"
            "2. Provide the title of the recipe\n"
            "3. Provide the required ingredients to make this recipe.\n"
            "4. Provide all steps to make this recipe (step-by-step).\n"
            "5. If the title of recipe contain a diet name, you have to strictly take the ingredients that fit to diet\n"
            "Return a JSON object with:\n"
            "title: Title of recipe.\n"
            "ingredients: A list of ingredient names as simple strings\n"
            "steps: Steps required to follow the recipe. step_number starts from 1 and is incremented by 1.\n"
            "Example:\n"
            '{"title": "Tortilla with chicken and vegetables",'
            '"ingredients": ["Chicken", "Onion", "Tomato", "Chinese cabbage", "Corn", "Cheese", "Tortillas"],'
            '"steps": [{"step_number": 1, "instruction": "Cut the vegetables"}, {"step_number": 2, "instruction": "Cut the chicken"}, {"step_number": 3, "instruction": "Season the chicken"}, {"step_number": 4, "instruction": "Fry the chicken"}, {"step_number": 5, "instruction": "Heat the tortillas"}, {"step_number": 6, "instruction": "Roll up the tortilla with the ingredients inside"}]}\n'
            "Respond ONLY with valid JSON."
        )

        result = self.llm.call_model_json(prompt)
        recipe_response = RecipeResponse(**result)
        return recipe_response