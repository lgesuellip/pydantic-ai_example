from pydantic_ai import Agent, RunContext
from core.expenses_tool import get_expenses_tool
from core.meals_tool import set_meal_tool
from core.models import AgentDeps
from jinja2 import Template
from dotenv import load_dotenv
import logfire


load_dotenv()
logfire.configure()

expenses_agent = Agent(
        "openai:gpt-4o",
        deps_type=AgentDeps,
        system_prompt=Template("""
        Eres un experto en gestionar los gastos del Equipo. Tus respuestas deben ser en argentino.
        """).render(),
        tools=[get_expenses_tool]
    )

async def transfer_to_expenses_agent(ctx: RunContext[AgentDeps], message: str) -> Agent:
    """
    Transfer control to the Expenses Agent for handling expenses-related tasks.
    """
    result = await expenses_agent.run(
        message, 
        deps=ctx.deps
    )
    return result

meal_agent = Agent(
        "openai:gpt-4o",
        deps_type=AgentDeps,
        tools=[set_meal_tool],
        system_prompt=Template("""
        Eres un experto en planificar pedidos de comidas para el Equipo, 
        tus respuesta deben ser claras, directas y en argentino.
        """).render()
    )

async def transfer_to_meal_agent(ctx: RunContext[AgentDeps], message: str) -> Agent:
    """
    Transfer control to the Meal Agent for handling meal-related tasks.
    """
    result = await meal_agent.run(
        message,
        deps=ctx.deps
    )
    return result


main_agent = Agent(
    "openai:gpt-4o",
    deps_type=AgentDeps,
    system_prompt=Template("""
    <Task>
    Tu nombre es Gabriela y sos un asistente de IA diseñado para ayudar al equipo de Pampa Labs. 
    </Task>

    <Guidelines>                   
    Tus respuestas deben ser:

    1. Amigables y accesibles, usando un tono cálido
    2. Concisas y al grano, evitando verbosidad innecesaria
    3. Útiles e informativas, proporcionando información precisa
    4. Respetuosas de la privacidad del usuario y los límites éticos
    </Guidelines>
    
    <Tools>
    Solo puedes ayudar usando las herramientas disponibles y con pedidos que vengan de miembros del equipo. 
    Todo lo que no se pueda responder usando las herramientas, debes decir que no puedes ayudar y disculparte.
    </Tools>
    """).render(),
    tools=[transfer_to_expenses_agent, transfer_to_meal_agent]
)

async def main():

    result = await main_agent.run(
        'I want to set the meal plan for the date 2024-05-01. The meal is lasagna.', 
        deps=AgentDeps(user_id='user1')
    )
    print(f"Data: {result.data}")
    print(f"All messages: {result.all_messages()}")

    result = await main_agent.run(
        'I want to get the expenses.', 
        deps=AgentDeps(user_id='user1')
    )
    print(f"Data: {result.data}")
    print(f"All messages: {result.all_messages()}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
