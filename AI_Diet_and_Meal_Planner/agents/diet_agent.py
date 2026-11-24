from models import DietResponse
from services.llm_client import LLMClient

class DietAgent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, items: list[str], diet: str) -> DietResponse:
        prompt = (
            f"You are a professional nutritionist. Given the JSON array of ingredients and a specific diet:\n"
            f"Ingredients: {items}\n"
            f"Diet: {diet}\n"
            "Rules:\n"
            "1. Check each ingredient separately against the diet.\n"
            "2. Remove ONLY the ingredients that the diet clearly forbids.\n"
            "3. Keep ALL other ingredients. If you are not sure, keep the ingredient.\n"
            "4. Suggest exactly 5 recipe ideas.\n"
            "5. Recipes may use ONLY ingredients from compatible_items. "
            "Do not add other main ingredients.\n"
            "6. Recipes must follow the diet (for example, no omelette in a vegan diet).\n\n"
            "compatible_items: all input ingredients except the forbidden ones.\n"
            "suggested_recipe_ideas: exactly 5 recipe names.\n"
            "Respond ONLY with valid JSON."
        )

        result = self.llm.call_model_json(prompt)
        diet_response = DietResponse(**result)
        return diet_response