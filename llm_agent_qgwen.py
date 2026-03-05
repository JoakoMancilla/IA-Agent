from langchain_fireworks import ChatFireworks
from langchain_core.messages import HumanMessage, ToolMessage
from tools import *


class LLMAgentQgwen():

    def __init__(self):

        self.llm = ChatFireworks(
            model="accounts/fireworks/models/qwen3-8b",
            temperature=0,
            max_tokens=1024,
        )

        self.llm = self.llm.bind_tools([
            promedio_de_notas,
            fetch_url,
        ])

        self.messages = []

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