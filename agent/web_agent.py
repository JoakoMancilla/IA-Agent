from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage
import re

from langfuse import Langfuse

from tools.web_tools import fetch_url

langfuse = Langfuse()


def _get_user_message(state: dict):
    return next(
        (m for m in reversed(state["messages"]) if isinstance(m, HumanMessage)),
        state["messages"][-1],
    )


def crear_web_agent(model):

    try:
        system_prompt = langfuse.get_prompt("webAgent").compile()
        if not system_prompt:
            raise ValueError("El prompt retornó vacío")
    except Exception as e:
        print(f"[web_agent] ERROR al cargar prompt desde Langfuse: {e}")
        raise

    agent = create_agent(
        model=model,
        system_prompt=system_prompt,
        tools=[fetch_url],
    )

    def limpiar_think(texto: str) -> str:
        return re.sub(r"<think>.*?</think>", "", texto, flags=re.DOTALL).strip()

    def web_node(state: dict):
        user_msg = _get_user_message(state)
        response = agent.invoke({"messages": [user_msg]})
        content = limpiar_think(response["messages"][-1].content)
        return {
            "messages": [AIMessage(content=content, name="web_agent")],
            "next": "supervisor"
        }

    return web_node