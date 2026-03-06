import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools import tool

from rich.console import Console
from rich.align import Align
from rich.text import Text

console = Console()

# --- CONFIGURACIÓN DE POSTGRES ---
# Cambia 'tu_password' por la que pusiste al instalar Postgres
CONNECTION_STRING = "postgresql+psycopg://postgres:7567@localhost:5432/postgres"
COLLECTION_NAME = "inacap_vader_docs"

_vector_store = None

EXTENSIONES_PERMITIDAS = {
    ".pdf": PyPDFLoader,
    ".txt": TextLoader,
    ".py": TextLoader,
    ".js": TextLoader
}

DIRECTORIOS_IGNORADOS = {"node_modules", ".git", ".venv", "venv", "__pycache__", "build", "dist"}

def _cargar_archivo(ruta_archivo: Path) -> list:
    ext = ruta_archivo.suffix.lower()
    if ext in EXTENSIONES_PERMITIDAS:
        try:
            loader_class = EXTENSIONES_PERMITIDAS[ext]
            loader = loader_class(str(ruta_archivo))
            return loader.load()
        except Exception as e:
            console.print(f"[red]Error cargando {ruta_archivo}: {e}[/red]")
    return []

def inicializar_rag(rutas: list[str]):
    """
    Carga archivos en PostgreSQL con pgvector usando embeddings locales.
    """
    global _vector_store
    
    console.print(Align.center(Text("⚙ Inicializando Sistema RAG en PostgreSQL...", style="dim")))
    
    # 1. Embeddings Locales (Familia Qwen) - No más error 429
    # La primera vez tardará un poco mientras descarga el modelo (~1.5GB)
    embeddings = HuggingFaceEmbeddings(
        model_name="Alibaba-NLP/gte-Qwen2-1.5B-instruct",
        model_kwargs={"device": "cpu"} # Pon "cuda" si tienes tarjeta NVIDIA
    )

    # 2. Conectar a PGVector
    _vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        use_jsonb=True,
    )

# 3. Procesamiento de archivos
    if rutas:
        documentos_cargados = []
        for ruta_str in rutas:
            ruta = Path(ruta_str)
            if ruta.is_file():
                documentos_cargados.extend(_cargar_archivo(ruta))
            elif ruta.is_dir():
                for root, dirs, files in os.walk(ruta):
                    dirs[:] = [d for d in dirs if d not in DIRECTORIOS_IGNORADOS]
                    for file in files:
                        documentos_cargados.extend(_cargar_archivo(Path(root) / file))

        if documentos_cargados:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            splits = text_splitter.split_documents(documentos_cargados)
            _vector_store.add_documents(splits)
            console.print(f"[green]✓ {len(splits)} fragmentos añadidos a la base de datos.[/green]")
        else:
            console.print("[yellow]⚠ Se pasaron rutas pero no se encontraron documentos válidos.[/yellow]")
    else:
        # Si la lista de rutas está vacía desde el inicio
        console.print("[cyan]ℹ Iniciando en modo consulta: Usando datos existentes en Postgres.[/cyan]")   

@tool
def consultar_documentos(query: str) -> str:
    """
    Busca información en los archivos locales (PDF, código, apuntes) 
    almacenados en la base de datos vectorial del Imperio.
    """
    console.print(Align.right(Text("⚙ TOOL: consultar_documentos (Postgres)", style="bold #c4b5fd")))
    
    if _vector_store is None:
        return "Error: La base de datos vectorial no está conectada."

    # Búsqueda de similitud
    retrieved_docs = _vector_store.similarity_search(query, k=4)

    if not retrieved_docs:
        return "No encontré nada en mis archivos sobre eso."

    contexto = "\n\n".join(
        f"--- Fuente: {doc.metadata.get('source', 'Desconocido')} ---\n{doc.page_content}"
        for doc in retrieved_docs
    )
    return contexto