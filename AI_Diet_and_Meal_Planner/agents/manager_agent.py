from agents.diet_agent import DietAgent
from agents.inventory_agent import InventoryAgent
from models import AskResponse


class ManagerAgent:
    def __init__(self):
        self.InventoryAgent = InventoryAgent()
        self.Diet = DietAgent()

    def run(self, items: list[str], diet: str) -> AskResponse:
        inventory_result = self.InventoryAgent.run(items)
        filtered_items = self.Diet.run(inventory_result.usable_items, diet)
        return AskResponse(usable_items=inventory_result.usable_items, diet_filtered=filtered_items.compatible_items, suggestions=filtered_items.suggested_recipe_ideas)

