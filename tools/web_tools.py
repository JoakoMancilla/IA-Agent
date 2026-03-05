from langchain.tools import tool
import requests

from bs4 import BeautifulSoup

from rich.align import Align
from rich.console import Console
from rich.text import Text
from rich.align import Align


console = Console()
    
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
