from typing import List
from pydantic import BaseModel
from pydantic_ai import RunContext
from core.models import AgentDeps

import logging
logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)


class Expense(BaseModel):
    expense_type: str
    date: str
    total_value: float
    state: str

class UserExpenses(BaseModel):
    expenses: List[Expense]

def get_expenses_tool(ctx: RunContext[AgentDeps]) -> str:
    """
    Retrieves all pending expenses
    """
    logger.debug(f"Context: {ctx}")
    # Mock implementation for testing purposes
    mock_expenses = {
        "user1": UserExpenses(
            expenses=[
                Expense(
                    expense_type="food",
                    date="2023-05-01",
                    total_value=50.0,
                    state="pending"
                ),
                Expense(
                    expense_type="coffee",
                    date="2023-05-02",
                    total_value=5.0,
                    state="pending"
                )
            ]
        )
    }
    return f"Expenses retrieved: {mock_expenses[ctx.deps.user_id].expenses}"
