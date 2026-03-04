from langchain.tools import tool
from rich.align import Align
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
console = Console()

@tool
def promedio_de_notas(notas: list[float]) -> float:
    """
    Usa esta herramienta cuando el usuario quiera calcular el promedio de notas.

    El usuario debe entregar una lista de números.

    Ejemplo:
    [5.5, 6.0, 4.0]
    """
    console.print(
        Align.right(
            Text("⚙ TOOL: promedio_de_notas ejecutado", style="bold #c4b5fd")
        )
    )

    #sumamos todas las notas que nos llegan con un iterador
    suma_notas = 0
    for i in notas:
        suma_notas += i

    #calculamos la cantidad de notas
    cantidad_notas = len(notas)

    if cantidad_notas > 0:
        #dividimos la suma de las notas en la cantidad de notas
        resultado = suma_notas / cantidad_notas

        return resultado

    else:
        print("Error: Ingresa almenos 2 notas")

        return