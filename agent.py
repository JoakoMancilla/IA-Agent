from dotenv import load_dotenv
from llm_agent import LLMAgent
from os import system
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.rule import Rule
from rich.padding import Padding

console = Console()

COLOR_FADE = "#ddd6fe"
COLOR_SOFT = "#c4b5fd"
COLOR_MAIN = "#601EF8"

load_dotenv()
agent = LLMAgent()

system("cls")


# =========================
# FUNCIONES GRADIENTE
# =========================

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0,2,4))


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def interpolate(c1, c2, factor):
    return tuple(
        int(c1[i] + (c2[i] - c1[i]) * factor)
        for i in range(3)
    )


def vertical_gradient(text, palette):
    lines = text.split("\n")
    rgb_palette = [hex_to_rgb(c) for c in palette]
    result = Text()
    total_lines = len(lines)

    for i, line in enumerate(lines):
        position = i / max(total_lines - 1, 1)
        segment = position * (len(rgb_palette) - 1)
        left = int(segment)
        right = min(left + 1, len(rgb_palette) - 1)
        factor = segment - left

        color = rgb_to_hex(interpolate(rgb_palette[left], rgb_palette[right], factor))
        result.append(line + "\n", style=color)

    return result


# =========================
# PALETA DE MARCA
# =========================

brand_gradient = [
    "#A06AF9",
    "#8B4DF8",
    "#7832F7",
    "#6C28F7",
    "#601EF8",
    "#5B1AF8",
    "#5313F8",
    "#4A0BF8"
]


# =========================
# LOGO
# =========================

logo_ascii = """
    ▄▄▄▄
    ████
████    
████▆▆▆▆
████████
▀▀▀▀▀▀▀▀
"""

logo = vertical_gradient(logo_ascii, brand_gradient)

header_title = Text.assemble(
    logo,
    Text("\nIA-Agent\n", style="bold white"),
    Text("By JoakoDev", style="dim")
)


# =========================
# HEADER PRINCIPAL
# =========================

console.print()
console.print(
    Panel(
        Align.center(header_title),
        border_style=COLOR_SOFT,
        padding=(1, 4),
        width=48,
    )
)
console.print(Rule(style=COLOR_FADE))

console.print(Text("▹ Escribe tu pregunta y presiona enter", style="dim"))
console.print(Text("▹ exit / q para salir", style="dim"))
console.print()


# =========================
# LOOP PRINCIPAL
# =========================

while True:

    pregunta = console.input(
        f"[bold white]You[/bold white] [bold {COLOR_MAIN}]›[/bold {COLOR_MAIN}] "
    )

    if pregunta.lower() in ["exit", "q"]:
        console.print("\n[dim]Cerrando agente...[/dim]")
        break

    console.print()
    respuesta = agent.ask(pregunta)

    console.print(
        Panel(
            Padding(respuesta, (0, 1)),
            title="[bold white]IA-Agent[/bold white]",
            title_align="left",
            border_style=COLOR_SOFT,
            padding=(1, 2),
        )
    )

    console.print(Rule(style=COLOR_FADE))
    console.print()