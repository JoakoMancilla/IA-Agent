from dotenv import load_dotenv
from llm_agent import LLMAgent
from os import system

#Con esto cargamos el .env que es quien guarda la APIKEY
load_dotenv()

agent = LLMAgent()

system("cls")
print("========IA-Agent By JoakoDev========\n")

print("====================================")
print("|      Agente de IA iniciado       |")
print("|    escribe 'exit' para salir.    |")
print("====================================\n")

while True:

    pregunta = input("Tu: ")

    if pregunta.lower() == "exit":
        print('Cerrando Agente...')
        break

    # Invocamos al LLM entregandole 'pregunta' como parametro y su respuesta la guardaresmos en la varible 'respuesta'
    respuesta = agent.ask(pregunta)

    print(f"\nIA: {respuesta}")
    print()
