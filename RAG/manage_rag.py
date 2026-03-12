import os
from os import system
from dotenv import load_dotenv
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from rich.console import Console
from rich.align import Align
from rich.text import Text

#cargamos la API_KEY de GEMINI
load_dotenv()


console = Console()

# --- CONFIGURACIÓN POSTGRES ---
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


def conectar_vector_store():
    """
    Conecta con PostgreSQL + pgvector
    """
    global _vector_store

    #Modelo de embedding principal: gemini
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    #Modelo de embedding de hugginface 
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="Alibaba-NLP/gte-Qwen2-1.5B-instruct",
        model_kwargs={"device": "cpu"}
    )
    """
    _vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        use_jsonb=True,
    )
    system("cls")
    console.print("[green]✓ Vector Store conectado[/green]")


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
    Indexa documentos en la base vectorial
    """

    global _vector_store

    system("cls")

    console.print(Align.center(Text("⚙ Inicializando Sistema RAG en PostgreSQL...", style="dim")))

    if _vector_store is None:
        conectar_vector_store()

    documentos_cargados = []

    for ruta_str in rutas:

        ruta = Path(ruta_str)

        if ruta.is_file():
            documentos_cargados.extend(_cargar_archivo(ruta))

        elif ruta.is_dir():
            for root, dirs, files in os.walk(ruta):

                dirs[:] = [d for d in dirs if d not in DIRECTORIOS_IGNORADOS]

                for file in files:
                    documentos_cargados.extend(
                        _cargar_archivo(Path(root) / file)
                    )

    if not documentos_cargados:
        console.print("[yellow]⚠ No se encontraron documentos válidos[/yellow]")
        return

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 700,
        chunk_overlap = 150
    )

    splits = text_splitter.split_documents(documentos_cargados)

    _vector_store.add_documents(splits)

    console.print(f"[green]✓ {len(splits)} fragmentos añadidos[/green]")


def get_vector_store():
    return _vector_store