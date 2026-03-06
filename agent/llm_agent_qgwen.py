from langchain_fireworks import ChatFireworks
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage

from tools.math_tools import promedio_de_notas
from tools.web_tools import fetch_url
from tools.rag_tool import consultar_documentos


class LLMAgentQgwen():

    def __init__(self):

        self.llm = ChatFireworks(
            model="accounts/fireworks/models/qwen3-8b",
            temperature=0.1,
            max_tokens=1024,
        )

        self.llm = self.llm.bind_tools([
            promedio_de_notas,
            fetch_url,
            consultar_documentos
        ])

        self.messages = [
            SystemMessage(content="""Eres un asistente experto en programación. 
            TIENES ACCESO a una base de datos local llamada 'inacap_vader_docs'. 
            Antes de responder sobre archivos como 'models.py', 'views.py' o apuntes, 
            DEBES usar la herramienta 'consultar_documentos' para ver el código real. 
            No inventes código si puedes consultarlo.""")
        ]

        print("LLM inicializado")


    def ask(self, pregunta):

        #Esta funcion nos permite limitar el historial para que
        #  el prompt no sea masivo despues de unas cuantas preguntas
        if len(self.messages) > 12:
            self.messages = self.messages[-12:]

        self.messages.append(HumanMessage(content=pregunta))
        response = self.llm.invoke(self.messages)
        self.messages.append(response)

        # Si el modelo quiere usar herramientas
        if response.tool_calls:

            for tool_call in response.tool_calls:

                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                if tool_name == "promedio_de_notas":
                    result = promedio_de_notas.invoke(tool_args)

                elif tool_name == "fetch_url":
                    result = fetch_url.invoke(tool_args)

                elif tool_name == "consultar_documentos":
                    result = consultar_documentos.invoke(tool_args)

                else:
                    result = "Herramienta no encontrada"

                self.messages.append(
                    ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call["id"],
                    )
                )

            final_response = self.llm.invoke(self.messages)

            self.messages.append(final_response)

            return final_response.content or ""

        else:
            return response.content or ""