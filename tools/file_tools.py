from pathlib import Path
from langchain.tools import tool
from tool_log import log_tool


WORKSPACE_ROOT = Path("C:/Joaquin/5.Personal").resolve()
WORKSPACE_ROOT.mkdir(exist_ok=True)


def _resolver_path(ruta: str) -> Path:
    """
    Convierte una ruta relativa en absoluta dentro del workspace.
    Lanza ValueError si intenta escapar del directorio raíz (path traversal).
    """
    path = (WORKSPACE_ROOT / ruta).resolve()
    if not str(path).startswith(str(WORKSPACE_ROOT)):
        raise ValueError(f"Acceso denegado: '{ruta}' está fuera del workspace.")
    return path


def _pedir_confirmacion(operacion: str, detalle: str) -> bool:
    """Deshabilitado temporalmente para depuración — siempre confirma."""
    return True


# ─────────────────────────────────────────
# TOOL 1 — Listar archivos
# ─────────────────────────────────────────
@tool
def listar_archivos(subdirectorio: str = "") -> str:
    """
    Lista los archivos y carpetas dentro del workspace.
    Parámetro opcional: subdirectorio (ruta relativa dentro del workspace).
    Ejemplo: listar_archivos("") → raíz del workspace
             listar_archivos("proyecto/src") → contenido de esa carpeta
    """
    log_tool("⚙ TOOL: listar_archivos ejecutado")

    try:
        carpeta = _resolver_path(subdirectorio)
    except ValueError as e:
        return str(e)

    if not carpeta.exists():
        return f"El directorio '{subdirectorio or '/'}' no existe en el workspace."

    if not carpeta.is_dir():
        return f"'{subdirectorio}' no es un directorio."

    # Human-in-the-loop
    ruta_display = subdirectorio or "(raíz del workspace)"
    if not _pedir_confirmacion("listar_archivos", f"Listar contenido de: {ruta_display}"):
        return "Operación cancelada por el usuario."

    entries = sorted(carpeta.iterdir())

    if not entries:
        return f"El directorio '{ruta_display}' está vacío."

    lineas = [f"📁 Contenido de: {ruta_display}", ""]
    for entry in entries:
        ruta_relativa = entry.relative_to(WORKSPACE_ROOT)
        if entry.is_dir():
            lineas.append(f"  📂 {ruta_relativa}/")
        else:
            tamaño = entry.stat().st_size
            lineas.append(f"  📄 {ruta_relativa}  ({tamaño} bytes)")

    return "\n".join(lineas)


# ─────────────────────────────────────────
# TOOL 2 — Leer archivo
# ─────────────────────────────────────────
@tool
def leer_archivo(ruta_archivo: str) -> str:
    """
    Lee el contenido de un archivo dentro del workspace.
    Parámetro: ruta_archivo (ruta relativa dentro del workspace).
    Ejemplo: leer_archivo("main.py")
             leer_archivo("src/utils.py")
    Solo permite leer archivos de texto (.py, .txt, .md, .json, .csv, .yaml, .env, .toml).
    """
    log_tool(f"⚙ TOOL: leer_archivo ejecutado → {ruta_archivo}")

    EXTENSIONES_PERMITIDAS = {".py", ".txt", ".md", ".json", ".csv", ".yaml", ".yml", ".toml", ".env"}

    try:
        archivo = _resolver_path(ruta_archivo)
    except ValueError as e:
        return str(e)

    if not archivo.exists():
        return f"El archivo '{ruta_archivo}' no existe en el workspace."

    if not archivo.is_file():
        return f"'{ruta_archivo}' no es un archivo."

    if archivo.suffix.lower() not in EXTENSIONES_PERMITIDAS:
        return (
            f"ERROR: No puedo leer '{ruta_archivo}'. "
            f"El formato '{archivo.suffix}' no es compatible con leer_archivo. "
            f"Solo soporto archivos de texto: {', '.join(sorted(EXTENSIONES_PERMITIDAS))}. "
            f"No inventes ni describas el contenido de este archivo."
        )

    # Human-in-the-loop
    if not _pedir_confirmacion("leer_archivo", f"Leer: {ruta_archivo}"):
        return "Operación cancelada por el usuario."

    try:
        contenido = archivo.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return f"No se pudo leer '{ruta_archivo}': el archivo no es texto UTF-8."

    if len(contenido) > 6000:
        contenido = contenido[:6000] + "\n\n[... contenido truncado a 6000 caracteres ...]"

    return f"--- {ruta_archivo} ---\n\n{contenido}"


# ─────────────────────────────────────────
# TOOL 3 — Moverse entre directorios
# Devuelve el árbol a partir de una carpeta
# ─────────────────────────────────────────
@tool
def explorar_directorio(subdirectorio: str = "", profundidad: int = 2) -> str:
    """
    Muestra el árbol de archivos y carpetas a partir de un subdirectorio,
    con profundidad configurable (máximo 3 niveles para no inundar el contexto).
    Parámetro: subdirectorio (ruta relativa), profundidad (1, 2 o 3).
    Ejemplo: explorar_directorio("", 2)  → árbol completo del workspace
             explorar_directorio("src", 1) → solo contenido directo de src/
    """
    log_tool(f"⚙ TOOL: explorar_directorio ejecutado → {subdirectorio or '/'}")

    profundidad = max(1, min(profundidad, 3))  # clamp entre 1 y 3

    try:
        carpeta = _resolver_path(subdirectorio)
    except ValueError as e:
        return str(e)

    if not carpeta.exists():
        return f"El directorio '{subdirectorio or '/'}' no existe en el workspace."

    # Human-in-the-loop
    ruta_display = subdirectorio or "(raíz del workspace)"
    if not _pedir_confirmacion(
        "explorar_directorio",
        f"Ver árbol de: {ruta_display}  (profundidad: {profundidad})"
    ):
        return "Operación cancelada por el usuario."

    lineas = [f"🗂  Árbol de: {ruta_display}", ""]

    def _arbol(path: Path, prefijo: str, nivel: int):
        if nivel > profundidad:
            return
        entries = sorted(path.iterdir())
        for i, entry in enumerate(entries):
            es_ultimo = (i == len(entries) - 1)
            conector = "└── " if es_ultimo else "├── "
            nombre = entry.name + ("/" if entry.is_dir() else "")
            lineas.append(f"{prefijo}{conector}{nombre}")
            if entry.is_dir():
                extensión = "    " if es_ultimo else "│   "
                _arbol(entry, prefijo + extensión, nivel + 1)

    _arbol(carpeta, "", 1)
    return "\n".join(lineas)