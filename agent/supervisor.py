from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

from langfuse import Langfuse

from rich.console import Console


console = Console()

langfuse = Langfuse()

#Hacemos la llamada del prompt directamente desde el workspace de langfuse
SYSTEM_PROMPT = langfuse.get_prompt("Supervisor").compile()
VALID_AGENTS = ["rag_agent", "math_agent", "web_agent", "file_agent"]




def _get_user_message(state: dict):
    return next(
        (m for m in reversed(state["messages"]) if isinstance(m, HumanMessage)),
        state["messages"][-1],
    )


def crear_supervisor(model):

    def supervisor_node(state: dict) -> dict:
        plan = state.get("plan", [])
        step = state.get("step", 0)

        # ── Fase 2: seguir plan ──
        if plan and step < len(plan):
            next_agent = plan[step]
            return {
                "next": next_agent,
                "plan": plan,
                "step": step + 1,
            }

        # ── Fase 3: sintetizar ──
        if plan and step >= len(plan):
            agent_results = [
                m for m in state["messages"]
                if hasattr(m, "name") and m.name in VALID_AGENTS
            ]
            if agent_results:

                def limpiar_think(texto: str) -> str:
                    import re
                    return re.sub(r"<think>.*?</think>", "", texto, flags=re.DOTALL).strip()

                # ── NUEVO: si solo respondió un agente, pasa directo sin invocar el modelo ──
                if len(agent_results) == 1:
                    answer = limpiar_think(agent_results[-1].content)
                    return {
                        "messages": [AIMessage(content=answer, name="supervisor")],
                        "next": "FINISH",
                        "plan": [],
                        "step": 0,
                    }

                # ── Si respondieron múltiples agentes, sintetiza normalmente ──
                agent_summaries = "\n\n".join([
                    f"[{m.name}]:\n<data>\n{limpiar_think(m.content)}\n</data>"
                    for m in agent_results
                ])

                historial_limpio = [
                    m for m in state["messages"]
                    if isinstance(m, HumanMessage)
                    or (hasattr(m, "name") and m.name == "supervisor")
                ]

                prompt_text = langfuse.get_prompt("supervisor-synthesis").compile()
                synthesis_template = prompt_text.replace("{agent_summaries}", agent_summaries)

                synthesis_prompt = [
                    SystemMessage(content=synthesis_template),
                    *historial_limpio,
                ]

                response = model.invoke(synthesis_prompt)
                answer = limpiar_think(response.content.strip())

                return {
                    "messages": [AIMessage(content=answer, name="supervisor")],
                    "next": "FINISH",
                    "plan": [],
                    "step": 0,
                }

        # ── Fase 1: crear plan ──
        user_question = _get_user_message(state)
        history = state["messages"]

        response = model.invoke([SystemMessage(content=SYSTEM_PROMPT), user_question])
        decision = response.content.strip().lower()

        def _direct_response(history):
            direct_prompt = [
                SystemMessage(content="You are a helpful assistant. Answer the user's question directly and concisely. Respond in the same language the user used."),
                *history,
            ]
            resp = model.invoke(direct_prompt)
            return {
                "messages": [AIMessage(content=resp.content, name="supervisor")],
                "next": "FINISH",
                "plan": [],
                "step": 0,
            }

        if "finish" in decision and not any(a in decision for a in VALID_AGENTS):
            return _direct_response(history)

        new_plan = [a for a in decision.replace(" ", "").split(",") if a in VALID_AGENTS]

        if not new_plan:
            return _direct_response(history)


        return {
            "next": new_plan[0],
            "plan": new_plan,
            "step": 1,
        }

    return supervisor_node