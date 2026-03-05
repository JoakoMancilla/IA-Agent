from langchain.tools import tool
import requests

from bs4 import BeautifulSoup

from rich.align import Align
from rich.console import Console
from rich.text import Text
from rich.align import Align


console = Console()

@tool
def promedio_de_notas(notas: list[float]) -> float:
    """
    Usa esta herramienta cuando el usuario quiera calcular el promedio de notas.
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
    
@tool
def fetch_url(url: str) -> str:
    """Fetch text content from a URL"""
    console.print(
        Align.right(
            Text("⚙ TOOL: fetch_url ejecutado", style="bold #c4b5fd")
        )
    )
    respuesta = requests.get(url, timeout=5.0)
    respuesta.raise_for_status()

    #Esto nos permite limpiar la pagina web y no traer texto inecesario 
    #Con la finalidad de optimizar el uso de tokens
    soup = BeautifulSoup(respuesta.text, "html.parser")

    text = soup.get_text(separator=" ", strip=True)

    return text[:4000]   # límite
