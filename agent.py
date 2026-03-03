import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

print("======IA-Agent By JoakoDev======")

#Con esto cargamos el .env que es quien guarda la APIKEY
load_dotenv()


#MAIN
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
)

print("====== Agente de IA iniciado ======")
print("escribe 'exit' para salir.")
while True:

    pregunta = input("Tu: ")

    if pregunta.lower() == "exit":
        print('Cerrando Agente...')
        break

    # Invocamos al LLM entregandole 'pregunta' como parametro y su respuesta la guardaresmos en la varible 'respuesta'
    respuesta = llm.invoke(pregunta)

    print(f"\nIA: {respuesta.content}")
    print()
