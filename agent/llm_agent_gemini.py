from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from tools.math_tools import promedio_de_notas
from tools.web_tools import fetch_url
from tools.rag_tool import consultar_documentos

class LLMAgentGemini:
    def __init__(self):
        
        #Modelo
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0
        )

        #Memoria
        self.memory = InMemorySaver()

        #Crear al agente
        self.agent = create_agent(
            model=self.model,
            system_prompt=
            """
            You are an assistant that can search information in local documents.
            If the user asks about documents, files, classes, notes, PDFs or code,
            you MUST use the tool consultar_documentos to search the knowledge base.
            """,
            tools=[
                promedio_de_notas,
                fetch_url,
                consultar_documentos
                ],
            checkpointer=self.memory
        )

        #ID conversacion
        self.config = {
            "configurable": {"thread_id": "1"}
        }

    def ask(self, pregunta):

        response = self.agent.invoke(
            {
                "messages":[
                    {
                        "role":"user",
                        "content":pregunta
                     }
                ]
            },
            config=self.config
        )
        content = response["messages"][-1].content

        # Si viene como lista (Gemini suele hacerlo)
        if isinstance(content, list):
            return content[0]["text"]
        
        return content