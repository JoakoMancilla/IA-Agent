from dotenv import load_dotenv
from os import system
import threading

from langchain_core.messages import HumanMessage

from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.rule import Rule
from rich.padding import Padding
from rich.console import Group
from rich.live import Live

import time
import uuid

from graph.graph_manage import crear_grafo
from tool_log import flush_tools   # <-- nuevo import

console = Console()

COLOR_FADE = "#ddd6fe"
COLOR_SOFT = "#c4b5fd"
COLOR_MAIN = "#601EF8"
COLOR_BG   = "#f6f5fd"
COLOR_DIM  = "#6d6a85"

load_dotenv()

grafo = crear_grafo()
config = {"configurable": {"thread_id": str(uuid.uuid4())}, "recursion_limit": 8}

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
            ("Fireworks AI", f"bold {COLOR_SOFT}"),
            (" ⦣V∠", COLOR_MAIN),
        )
    ),

    Align.center(Text("By JoakoMancillaDev", style="dim")),
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


# Funcion para tipeo — ahora recibe los tool logs opcionales
def type_panel(text, speed=0.01, tool_logs=None):
    output = ""

    # Construye el encabezado de tools (se muestra fijo, no se tipea)
    def build_panel(content):
        body_parts = []

        if tool_logs:
            for msg in tool_logs:
                t = Text()
                t.append(msg, style=f"dim {COLOR_SOFT}")
                body_parts.append(t)
            body_parts.append(Text(""))  # separador

        body_parts.append(Text(content))

        return Panel(
            Padding(Group(*body_parts), (0, 1)),
            title="[bold white]IA-Agent[/bold white]",
            border_style=COLOR_SOFT,
            padding=(1, 2),
        )

    with Live(refresh_per_second=30) as live:
        for char in text:
            output += char
            live.update(build_panel(output))
            time.sleep(speed)


# Spinner mientras el agente piensa
def thinking_spinner(done_event):
    thinking_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    idx = 0
    with Live(refresh_per_second=15) as live:
        while not done_event.is_set():
            live.update(
                Text.assemble(
                    (f" {thinking_frames[idx % len(thinking_frames)]} ", f"bold {COLOR_MAIN}"),
                    ("pensando...", f"dim {COLOR_DIM}"),
                )
            )
            time.sleep(0.08)
            idx += 1
        live.update(Text(""))


# MAIN
while True:
    try:
        pregunta = console.input(
            f"[bold white]You[/bold white] [bold {COLOR_MAIN}]›[/bold {COLOR_MAIN}] "
        )
        print(" ")
        if pregunta.lower() in ["exit", "q"]:
            system("cls")
            console.print()
            console.print(
                Panel(
                    Group(
                        Align.center(Text("◈", style=f"bold {COLOR_MAIN}")),
                        Text(""),
                        Align.center(Text("Cerrando agente...", style=f"bold {COLOR_BG}")),
                        Text(""),
                        Align.center(Text("Hasta pronto", style=f"dim {COLOR_DIM}")),
                    ),
                    border_style="#E1452B",
                    padding=(1, 2),
                    width=48,
                )
            )
            time.sleep(1.5)
            system("cls")
            break

        # Invoke con spinner en hilo separado
        state = {"resultado": None}
        done  = threading.Event()

        def invoke():
            state["resultado"] = grafo.invoke(
                {"messages": [HumanMessage(content=pregunta)]},
                config=config,
            )
            done.set()

        t = threading.Thread(target=invoke, daemon=True)
        t.start()
        thinking_spinner(done)

        # Recoge los mensajes de tools acumulados durante el invoke
        tool_logs = flush_tools()

        respuesta = state["resultado"]["messages"][-1].content
        type_panel(respuesta, 0.008, tool_logs=tool_logs)

        console.print()

    except Exception as e:
        error_msg = str(e)

        if "RESOURCE_EXHAUSTED" in error_msg:
            console.print(
                Align.center(
                    Text("⚙ ERROR: Límite de requests alcanzado", style="bold red")
                )
            )
            print("")
        else:
            print(f"ERROR: {error_msg}")
            console.print(
                Align.center(
                    Text(f"ERROR: {error_msg}", style="bold red")
                )
            )
            print("")