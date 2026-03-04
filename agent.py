from dotenv import load_dotenv
from llm_agent import LLMAgent
from os import system
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.rule import Rule
from rich.padding import Padding
from rich.console import Group

from rich.live import Live
import time


console = Console()

COLOR_FADE = "#ddd6fe"
COLOR_SOFT = "#c4b5fd"
COLOR_MAIN = "#601EF8"

load_dotenv()
agent = LLMAgent()

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

    Align.center(Text("Powered by Gemini", style="#c4b5fd")),

    Align.center(Text("By JoakoDev", style="dim")),
)

# HEADER
console.print(
    Panel(
        Align.center(header_title),
        title="[bold white]IA-Agent[/bold white]",
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
    respuesta = agent.ask(pregunta)

    type_panel(respuesta, 0.008)

    console.print()

