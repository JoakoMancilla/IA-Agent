from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage
import re

from langfuse import Langfuse

from tools.rag_tool import consultar_documentos

langfuse = Langfuse()


def _get_user_message(state: dict):
    return next(
        (m for m in reversed(state["messages"]) if isinstance(m, HumanMessage)),
        state["messages"][-1],
    )


def crear_rag_agent(model):

    try:
        system_prompt = langfuse.get_prompt("ragAgent").compile()
        if not system_prompt:
            raise ValueError("El prompt retornó vacío")
    except Exception as e:
        print(f"[rag_agent] ERROR al cargar prompt desde Langfuse: {e}")
        raise

    agent = create_agent(
        model=model,
        system_prompt=system_prompt,
        tools=[consultar_documentos],
    )

    def limpiar_think(texto: str) -> str:
        return re.sub(r"<think>.*?</think>", "", texto, flags=re.DOTALL).strip()

    def rag_node(state: dict):
        user_msg = _get_user_message(state)
        response = agent.invoke({"messages": [user_msg]})
        content = limpiar_think(response["messages"][-1].content)
        return {
            "messages": [AIMessage(content=content, name="rag_agent")],
            "next": "supervisor"
        }

    return rag_node