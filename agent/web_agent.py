from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage
import re

from tools.web_tools import fetch_url


def _get_user_message(state: dict):
    return next(
        (m for m in reversed(state["messages"]) if isinstance(m, HumanMessage)),
        state["messages"][-1],
    )


def crear_web_agent(model):

    agent = create_agent(
        model=model,
        system_prompt="""
You are a web scraping assistant. Your ONLY job is to fetch URLs and extract information.

You have ONE tool: fetch_url

MANDATORY RULES — no exceptions:
- If the user message contains a URL starting with http:// or https://, you MUST call fetch_url immediately.
- Do NOT think about whether you can access the internet. You CAN. fetch_url handles it.
- Do NOT say you lack internet access. You have fetch_url for that.
- Do NOT skip the tool call. Calling fetch_url is your primary purpose.
- Call fetch_url ONCE with the exact URL from the user message.
- After receiving the result, extract and return the relevant information.
- Return only the final extracted content. No disclaimers. No meta-commentary.
- Always answer in Spanish.
""",
        tools=[fetch_url],
    )

    def limpiar_think(texto: str) -> str:
        return re.sub(r"<think>.*?</think>", "", texto, flags=re.DOTALL).strip()

    def web_node(state: dict):
        user_msg = _get_user_message(state)

        response = agent.invoke({
            "messages": [user_msg]
        })

        content = limpiar_think(response["messages"][-1].content)

        return {
            "messages": [
                AIMessage(content=content, name="web_agent")
            ],
            "next": "supervisor"
        }

    return web_node