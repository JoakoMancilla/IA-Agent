from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage
import re

from tools.file_tools import listar_archivos, leer_archivo, explorar_directorio


def _get_user_message(state: dict):
    return next(
        (m for m in reversed(state["messages"]) if isinstance(m, HumanMessage)),
        state["messages"][-1],
    )


def crear_file_agent(model):

    agent = create_agent(
        model=model,
        system_prompt="""
You are a file system assistant. You help users navigate and read files inside a sandboxed workspace directory.

You have THREE tools:
- listar_archivos(subdirectorio)  : lists files and folders at a given path
- leer_archivo(ruta_archivo)      : reads the content of a text file
- explorar_directorio(subdirectorio, profundidad) : shows a directory tree

MANDATORY RULES:
- ALWAYS use a tool to answer. Never invent file names or contents.
- Start by listing or exploring if the user hasn't specified an exact file.
- Use leer_archivo only when you know the exact relative path of the file.
- You can call multiple tools in sequence (e.g. explore first, then read).
- Never try to access paths outside the workspace — the tools will block it.
- Always answer in Spanish.
- Return only the relevant content or summary. No disclaimers.

CRITICAL ANTI-HALLUCINATION RULES — these override everything else:
- If a tool returns an error, reproduce the error message exactly and stop. Do NOT invent content.
- If leer_archivo says a file extension is not supported, tell the user exactly that. Do NOT describe what the file might contain.
- If you cannot read a file for any reason, say "No puedo leer este archivo: [reason]". Never fabricate its contents.
- You only know what the tools return. If a tool gave you no data, you have no data.
""",
        tools=[listar_archivos, leer_archivo, explorar_directorio],
    )

    def limpiar_think(texto: str) -> str:
        return re.sub(r"<think>.*?</think>", "", texto, flags=re.DOTALL).strip()

    def file_node(state: dict):
        user_msg = _get_user_message(state)

        response = agent.invoke({
            "messages": [user_msg]
        })

        content = limpiar_think(response["messages"][-1].content)

        return {
            "messages": [
                AIMessage(content=content, name="file_agent")
            ],
            "next": "supervisor"
        }

    return file_node