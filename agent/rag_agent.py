from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage

from tools.rag_tool import consultar_documentos


def _get_user_message(state: dict):
    """Obtiene el HumanMessage original del usuario."""
    return next(
        (m for m in state["messages"] if isinstance(m, HumanMessage)),
        state["messages"][0],
    )


def crear_rag_agent(model):

    agent = create_agent(
        model=model,
        system_prompt="""
You are an AI assistant that answers questions using local documents.

You have access to the tool:

consultar_documentos
- searches a vector database of the user's personal documents
- includes CV, certificates, PDFs, and notes

IMPORTANT RULES:

If the user asks about:
- certificates
- CV
- personal documents
- courses
- studies

You MUST call the tool consultar_documentos before answering.

Never say you cannot access documents.

Always attempt to search the documents first.

After receiving the results, summarize the information clearly.

Answer in Spanish.
""",
        tools=[consultar_documentos],
    )

    def rag_node(state: dict):
        user_msg = _get_user_message(state)

        response = agent.invoke({
            "messages": [user_msg]
        })

        return {
            "messages": [
                AIMessage(content=response["messages"][-1].content, name="rag_agent")
            ],
            "next": "supervisor"
        }

    return rag_node