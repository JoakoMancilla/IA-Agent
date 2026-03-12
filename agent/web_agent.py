from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage

from tools.web_tools import fetch_url


def _get_user_message(state: dict):
    """Obtiene el HumanMessage original del usuario."""
    return next(
        (m for m in state["messages"] if isinstance(m, HumanMessage)),
        state["messages"][0],
    )


def crear_web_agent(model):

    agent = create_agent(
        model=model,
        system_prompt="""
You are a web assistant specialized in reading web pages.

Tool available:

fetch_url
- downloads the content of a webpage

Rules:

If the user provides a URL, call fetch_url ONCE.

After receiving the webpage content:
- extract the relevant information
- answer the question

Never call the tool more than once.

Do not loop.

Return only the final answer.

Always answer in Spanish.
""",
        tools=[fetch_url],
    )

    def web_node(state: dict):
        user_msg = _get_user_message(state)

        response = agent.invoke({
            "messages": [user_msg]
        })

        return {
            "messages": [
                AIMessage(content=response["messages"][-1].content, name="web_agent")
            ],
            "next": "supervisor"
        }

    return web_node