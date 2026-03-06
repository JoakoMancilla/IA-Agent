from dotenv import load_dotenv
from os import system

from agent.llm_agent_gemini import LLMAgentGemini
from agent.llm_agent_qgwen import LLMAgentQgwen

from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.rule import Rule
from rich.padding import Padding
from rich.console import Group
from rich.live import Live

import time

from tools.rag_tool import inicializar_rag

console = Console()

COLOR_FADE = "#ddd6fe"
COLOR_SOFT = "#c4b5fd"
COLOR_MAIN = "#601EF8"

load_dotenv()

# === NUEVO: INICIALIZAR RAG ===
# Puedes pasar un archivo directo y una carpeta entera.
rutas_a_cargar = [
    "C:/Joaquin/1.Academico/Inacap/4to Semestre 2025/Back-End", # Un directorio entero
]
inicializar_rag(rutas_a_cargar)
# ==============================


#Facilitamos la instancia de un 2do agente en caso de acabase los TOKENS
#EL Cambio debe realizarce manual en la Linea 118 que por defecto es: respuesta = agent.ask(pregunta)
agent_gemini = LLMAgentGemini()
agent_qgwen = LLMAgentQgwen()

system("cls")

# LOGO
header_title = Group(
    Align.center(Text("    ▄▄▄▄", style="#6F2EE7")),
    Align.center(Text("    ████", style="#6C28F7")),
    Align.center(Text("████    ", style="#601EF8")),
    Align.center(Text("████▆▆▆▆", style="#5B1AF8")),
    Align.center(Text("████████", style="#5313F8")),
    Align.center(Text("▀▀▀▀▀▀▀▀", style="#4A0BF8")),

    Text(""),

    Align.center(
        Text.assemble(
            ("Powered by: ", "#f6f5fd"),
            ("Gemini", f"bold {COLOR_SOFT}"),
            ("✦", COLOR_MAIN),
        )
    ),

    Align.center(Text("By JoakoDev", style="dim")),
)

# HEADER
console.print(
    Panel(
        Align.center(header_title),
        title="[bold #f6f5fd]IA-Agent[/bold #f6f5fd]",
        title_align="left",
        border_style=COLOR_SOFT,
        padding=(0, 0),
        width=48,
    )
)

console.print()
console.print(Text("▹ Escribe tu pregunta y presiona enter", style="dim"))
console.print(Text("▹ exit / q para salir", style="dim"))
console.print(Rule(style=COLOR_FADE))
console.print()

#Funcion para tipeo
def type_panel(text, speed=0.01):

    output = ""

    with Live(refresh_per_second=30) as live:

        for char in text:

            output += char

            live.update(
                Panel(
                    Padding(output, (0,1)),
                    title="[bold white]IA-Agent[/bold white]",
                    border_style=COLOR_SOFT,
                    padding=(1,2)
                )
            )

            time.sleep(speed)

# MAIN
while True:

    pregunta = console.input(
        f"[bold white]You[/bold white] [bold {COLOR_MAIN}]›[/bold {COLOR_MAIN}] "
    )

    if pregunta.lower() in ["exit", "q"]:
        system("cls")
        console.print(
            Panel(
                Align.center(Text("Cerrando agente...", style="bold red")),
                border_style='#E1452B',
                padding=(1, 2),
                width=48,
            )
        )
        time.sleep(1.5)
        system("cls")
        break

    console.print()
    respuesta = agent_qgwen.ask(pregunta)

    type_panel(respuesta, 0.008)

    console.print()

