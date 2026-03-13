from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from rich.console import Console
from rich.text import Text
from rich.align import Align

console = Console()

SYSTEM_PROMPT = """
You are a supervisor that decides which agents are needed to answer the user's request.

Available agents:
- rag_agent   : searches local documents (CV, certificates, PDFs, personal files)
- math_agent  : performs mathematical calculations and grade averages
- web_agent   : fetches content from the internet or a given URL. ONLY use if the user provides an explicit URL in their message.

Analyze ONLY the latest user message. Ignore previous conversation context.

Respond ONLY with the agent names needed, separated by commas.

Examples:
  web_agent
  rag_agent
  web_agent, rag_agent
  math_agent
  web_agent, rag_agent, math_agent

If no agents are needed (simple greeting, general question), respond with:
  FINISH

Rules:
- Evalue use an agent before generate the answer.
- Analyze ONLY the current message, not previous ones.
- Only include agents that are truly necessary for THIS message.
- web_agent: ONLY if the user explicitly provides a URL (http:// or https://) in their message. NEVER use for general knowledge questions.
- rag_agent: ONLY if the user asks about their own documents, CV, or certificates.
- math_agent: ONLY if the user asks for a calculation or average.
- For general knowledge, history, science, or any question without a URL and without personal documents → FINISH.
- Order matters: if web info is needed first, put web_agent before rag_agent.
"""

VALID_AGENTS = ["rag_agent", "math_agent", "web_agent"]


def _log(msg: str):
    console.print(Align.right(Text(msg, style="dim #7c6f9f")))


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
            _log(f"▹ {next_agent}  {step + 1}/{len(plan)}")
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

                agent_summaries = "\n\n".join([
                    f"[{m.name}]:\n{limpiar_think(m.content)}"
                    for m in agent_results
                ])

                # Solo historial humano + supervisor, sin mensajes de agentes intermedios
                historial_limpio = [
                    m for m in state["messages"]
                    if isinstance(m, HumanMessage)
                    or (hasattr(m, "name") and m.name == "supervisor")
                ]

                synthesis_prompt = [
                    SystemMessage(content=f"""You are a helpful assistant.
        The user asked a question. Specialized agents gathered the following information:

        {agent_summaries}

        Synthesize everything into a single clear answer in the same language the user used.
        Do not mention agent names or technical details."""),
                    *historial_limpio,
                ]

                response = model.invoke(synthesis_prompt)
                answer = limpiar_think(response.content.strip())

                _log("▹ sintetizando")
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

        _log(f"▹ {' → '.join(new_plan)}")
        return {
            "next": new_plan[0],
            "plan": new_plan,
            "step": 1,
        }

    return supervisor_node