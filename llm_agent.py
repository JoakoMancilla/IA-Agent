from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

class LLMAgent:
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
            system_prompt="You are a helpfull assistan",
            tools=[],
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
        return response["messages"][-1].content