from langchain.tools import tool

from rag.manage_rag import conectar_vector_store, get_vector_store

from rich.console import Console
from rich.align import Align
from rich.text import Text

console = Console()

# conectar al iniciar
conectar_vector_store()

@tool
def consultar_documentos(query: str) -> str:
    """
    Busca información en los archivos locales almacenados en la DB vectorial.
    """

    console.print(Align.right(Text("⚙ TOOL: consultar_documentos (Postgres)", style="bold #c4b5fd")))

    vector_store = get_vector_store()

    if vector_store is None:
        return "Error: La base vectorial no está conectada."

    retrieved_docs = vector_store.similarity_search(query, k=8)

    if not retrieved_docs:
        return "No encontré nada en mis archivos."

    contexto = "\n\n".join(
        f"--- Fuente: {doc.metadata.get('source','Desconocido')} ---\n{doc.page_content}"
        for doc in retrieved_docs
    )

    return contexto