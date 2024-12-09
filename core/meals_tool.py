from core.models import AgentDeps
from pydantic_ai import RunContext

def set_meal_tool(ctx: RunContext[AgentDeps], meal: str, date: str):
    """
    Sets the meal plan for a specific date.

    Args:
        meal (str): The name of the meal.
        date (str): The date of the meal plan.
    """
    return f"Meal plan created and sent to the provider: {meal} for {date} by team member {ctx.deps.user_id}"
