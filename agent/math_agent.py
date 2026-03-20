from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage

from tools.math_tools import promedio_de_notas


def _get_user_message(state: dict):
    """Obtiene el HumanMessage original del usuario."""
    return next(
        (m for m in reversed(state["messages"]) if isinstance(m, HumanMessage)),
        state["messages"][-1],
    )


def crear_math_agent(model):

    agent = create_agent(
        model=model,
        system_prompt="""
You are a mathematical assistant.

Your job is to solve numerical and mathematical problems.

You may receive questions about:
- averages
- sums
- multiplications
- divisions
- percentages
- statistics
- simple calculations

Rules:

If a calculation is required:
- compute the result carefully
- show the final result clearly

If a math tool is available, use it when appropriate.

Never guess numbers.

Important:
- Do NOT output internal reasoning.
- Do NOT use <think>.
- Return only the final result and a short explanation.

Always answer in Spanish.
""",
        tools=[promedio_de_notas],
    )

    def math_node(state: dict):
        user_msg = _get_user_message(state)

        response = agent.invoke({
            "messages": [user_msg]
        })

        return {
            "messages": [
                AIMessage(content=response["messages"][-1].content, name="math_agent")
            ],
            "next": "supervisor"
        }

    return math_node