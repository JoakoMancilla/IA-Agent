# tool_log.py
# Lista compartida donde las tools depositan sus mensajes.
# main.py la lee y vacía antes de mostrar la respuesta.

tool_messages: list[str] = []

def log_tool(msg: str) -> None:
    tool_messages.append(msg)

def flush_tools() -> list[str]:
    msgs = tool_messages.copy()
    tool_messages.clear()
    return msgs