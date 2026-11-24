from fastapi import FastAPI
from agents.planner_agent import PlannerAgent
from models import InventoryResponse, DietResponse, InventoryInput, DietInput, AskInput, AskResponse, PlanInput, \
    RecipeResponse, RecommendInput, RecommendResponse
from agents.inventory_agent import InventoryAgent
from agents.diet_agent import DietAgent
from agents.manager_agent import ManagerAgent
from logger import get_logger
app = FastAPI(title="AI Diet & Meal Planner")
inventory_agent = InventoryAgent()
diet_agent = DietAgent()
manager_agent = ManagerAgent()
planner_agent = PlannerAgent()
logger = get_logger("app")

@app.get("/")
def root():
    return {"message": "Success!"}

@app.post("/inventory")
def inventory(data: InventoryInput) -> InventoryResponse:
    inventory_response = inventory_agent.run(data.items)
    return inventory_response

@app.post("/diet")
def diet(data: DietInput) -> DietResponse:
    diet_response = diet_agent.run(data.items, data.diet)
    return diet_response

@app.post("/ask")
def ask(data: AskInput) -> AskResponse:
    logger.info("Received /ask request: items=%s, diet=%s", data.items, data.diet)
    agent_result = manager_agent.run(data.items, data.diet)
    logger.info("/ask suggestions: %s", agent_result.suggestions)
    return agent_result

@app.post("/plan")
def plan(data: PlanInput) -> RecipeResponse:
    logger.info("Received /plan request: base_recipe=%s", data.base_recipe)
    planner_result = planner_agent.run(data.base_recipe)
    logger.info("/plan response title: title=%s", planner_result.title)
    return planner_result

@app.post("/recommend")
def recommend(data: RecommendInput) -> RecommendResponse:
    logger.info("Received /recommend request: items=%s, diet=%s, recipe_count=%s", data.items, data.diet, data.recipe_count)
    result = []
    manager_result = manager_agent.run(data.items, data.diet)
    suggestions = manager_result.suggestions[:data.recipe_count]
    for suggestion in suggestions:
        planner_result = planner_agent.run(suggestion)
        result.append(planner_result)

    recommend_response = RecommendResponse(recipes=result)
    logger.info("/recommend response number of recipes: number=%s", len(recommend_response.recipes))
    return recommend_response

