# graph/graph_manage.py
from typing import TypedDict, Annotated, List
import operator

from langchain_fireworks import ChatFireworks
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from agent.supervisor import crear_supervisor
from agent.rag_agent import crear_rag_agent
from agent.math_agent import crear_math_agent
from agent.web_agent import crear_web_agent


# ─────────────────────────────────────────
# EL ESTADO — el cuaderno compartido
#
# messages : se ACUMULA con operator.add (nunca se sobreescribe)
# next     : el agente que toca ejecutar ahora, o "FINISH"
# plan     : lista completa de agentes decidida por el supervisor
#            ej: ["web_agent", "rag_agent"]
# step     : índice del próximo agente a ejecutar en el plan
#
# IMPORTANTE: plan y step deben estar declarados aquí.
# Si no están en el TypedDict, LangGraph los descarta silenciosamente
# cuando el estado pasa entre nodos — el supervisor los perdería
# en cada vuelta y nunca podría ejecutar el segundo agente.
# ─────────────────────────────────────────
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    next: str
    plan: List[str]
    step: int


def crear_grafo():

    # Modelo para el supervisor: instruct, sin reasoning
    model_supervisor = ChatFireworks(
        model="accounts/fireworks/models/llama-v3p3-70b-instruct",
        temperature=0,

    )

    # Modelo para los agentes especializados
    model_agentes = ChatFireworks(
        model="accounts/fireworks/models/qwen3-8b",
        temperature=0,

    )

    # Instanciamos los nodos
    supervisor_node = crear_supervisor(model_supervisor)
    rag_node        = crear_rag_agent(model_agentes)
    math_node       = crear_math_agent(model_agentes)
    web_node        = crear_web_agent(model_agentes)

    # Creamos el grafo con nuestro estado
    grafo = StateGraph(AgentState)

    # Registramos los nodos
    grafo.add_node("supervisor", supervisor_node)
    grafo.add_node("rag_agent",  rag_node)
    grafo.add_node("math_agent", math_node)
    grafo.add_node("web_agent",  web_node)

    # Edges fijos
    grafo.add_edge(START, "supervisor")
    grafo.add_edge("rag_agent",  "supervisor")
    grafo.add_edge("math_agent", "supervisor")
    grafo.add_edge("web_agent",  "supervisor")

    # Edge condicional — el supervisor decide a dónde ir según state["next"]
    grafo.add_conditional_edges(
        "supervisor",
        lambda state: state["next"],
        {
            "rag_agent":  "rag_agent",
            "math_agent": "math_agent",
            "web_agent":  "web_agent",
            "FINISH":     END,
        }
    )

    memory = InMemorySaver()
    return grafo.compile(checkpointer=memory)