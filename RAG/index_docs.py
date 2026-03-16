from os import system
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.rule import Rule
from rich.console import Group
from rich.live import Live
import threading
import time
import os

# ── CONFIG ────────────────────────────────────────────────────────────────────
console = Console()

COLOR_FADE = "#ddd6fe"
COLOR_SOFT = "#c4b5fd"
COLOR_MAIN = "#601EF8"
COLOR_BG   = "#f6f5fd"
COLOR_DIM  = "#6d6a85"

RUTAS = [
    #"C:/Joaquin/1.Academico/Certificados",
    "../docs/CV_JoaquinMancilla_2026_Febrero.pdf"
]

# ── UI ────────────────────────────────────────────────────────────────────────
def mostrar_header():
    console.print()
    console.print(
        Panel(
            Align.center(
                Text.assemble(
                    ("RAG", f"bold {COLOR_SOFT}"),
                    ("  ·  ", f"dim {COLOR_DIM}"),
                    ("Indexar documentos", COLOR_BG),
                )
            ),
            border_style=COLOR_FADE,
            padding=(0, 2),
            width=48,
        )
    )
    console.print()

def mostrar_rutas():
    for i, ruta in enumerate(RUTAS, start=1):
        existe = os.path.exists(ruta)
        console.print(
            Text.assemble(
                (f"  [{i}] ", f"bold {COLOR_SOFT}"),
                (ruta, COLOR_BG),
                ("  ✔", "bold green") if existe else ("  ✘", "bold red"),
            )
        )
    console.print()
    console.print(Rule(style=COLOR_FADE))
    console.print()
    console.print(Text("▹ Enter para continuar - exit / q para salir", style="dim"))
    console.print()

def mostrar_resultado(err):
    console.print()
    if err:
        console.print(
            Panel(
                Align.center(Text.assemble(("✘  ", "bold red"), (str(err), f"dim {COLOR_DIM}"))),
                border_style="red",
                padding=(0, 2),
                width=48,
            )
        )
        console.print()
    else:
        console.print(
            Panel(
                Align.center(Text.assemble(("◈  ", f"bold {COLOR_MAIN}"), (f"{len(RUTAS)} documento(s) indexado(s)", COLOR_BG))),
                border_style=COLOR_SOFT,
                padding=(0, 2),
                width=48,
            )
        )
        console.print()
        time.sleep(1.2)
        system("cls")

# ── LÓGICA ────────────────────────────────────────────────────────────────────
def ejecutar_indexacion():
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    done   = threading.Event()
    result = {"err": None}

    def worker():
        try:
            from manage_rag import inicializar_rag
            inicializar_rag(RUTAS)
        except Exception as e:
            result["err"] = e
        finally:
            done.set()

    threading.Thread(target=worker, daemon=True).start()

    with Live(refresh_per_second=15) as live:
        for i in range(int(1e9)):
            if done.is_set():
                break
            live.update(Text.assemble(
                (f"  {frames[i % len(frames)]} ", f"bold {COLOR_MAIN}"),
                ("indexando documentos...", f"dim {COLOR_DIM}"),
            ))
            time.sleep(0.08)
        live.update(Text(""))

    return result["err"]

def pedir_confirmacion():
    while True:
        accion = console.input(
            f"  [bold white]Index[/bold white] [bold {COLOR_MAIN}]›[/bold {COLOR_MAIN}] "
        ).strip().lower()

        if accion in ["exit", "q"]:
            return "salir"
        if accion in ["continuar", "c", ""]:
            return "continuar"

        console.print(Text("  Comando no reconocido.", style=f"dim {COLOR_DIM}"))
        console.print()

# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    system("cls")
    mostrar_header()
    mostrar_rutas()

    accion = pedir_confirmacion()

    if accion == "salir":
        system("cls")
        console.print()
        console.print(
            Panel(
                Align.center(Text.assemble(("◈  ", f"bold {COLOR_MAIN}"), ("Cancelado", f"dim {COLOR_DIM}"))),
                border_style="#E1452B",
                padding=(0, 2),
                width=48,
            )
        )
        console.print()
        time.sleep(0.8)
        system("cls")
        return

    console.print()
    err = ejecutar_indexacion()
    mostrar_resultado(err)

main()