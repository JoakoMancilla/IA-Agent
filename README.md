<div align="center">

```
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║     ██╗ █████╗         █████╗  ██████╗ ███████╗███╗  ██╗████████╗  ║
║     ██║██╔══██╗       ██╔══██╗██╔════╝ ██╔════╝████╗ ██║╚══██╔══╝  ║
║     ██║███████║█████╗ ███████║██║  ███╗█████╗  ██╔██╗██║   ██║     ║
║     ██║██╔══██║╚════╝ ██╔══██║██║   ██║██╔══╝  ██║╚████║   ██║     ║
║     ██║██║  ██║       ██║  ██║╚██████╔╝███████╗██║ ╚███║   ██║     ║
║     ╚═╝╚═╝  ╚═╝       ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚══╝   ╚═╝     ║
║                                                                    ║
║            Multi-Agent AI System · RAG · CLI · Langfuse            ║
╚════════════════════════════════════════════════════════════════════╝
```

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)](https://langchain.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Langfuse](https://img.shields.io/badge/Langfuse-Observability-FF6B35?style=for-the-badge&logo=grafana&logoColor=white)](https://langfuse.com)
[![Rich](https://img.shields.io/badge/Rich-CLI-7E57C2?style=for-the-badge&logo=gnometerminal&logoColor=white)](https://rich.readthedocs.io)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

</div>

<br>

```bash
$ python main.py
```

```
╭──────────────────────────────────────────────────────────────╮
│  IA-Agent v1.0  │  Multi-Agent · RAG · CLI                   │
│  Supervisor online · 4 sub-agents loaded · pgvector ready    │
╰──────────────────────────────────────────────────────────────╯

[supervisor] Agente listo. Escribe tu consulta o 'exit' para salir.

> _
```

<img width="1886" height="964" alt="Captura de pantalla 2026-03-12 231603" src="https://github.com/user-attachments/assets/05150759-8846-4b46-aa21-97063959813c" />

<br>

---

## `$ cat README.md`

**IA-Agent** es un sistema de inteligencia artificial conversacional que corre desde la terminal. Un **agente supervisor** recibe tus consultas y delega al sub-agente más adecuado — ya sea buscar en tus documentos, navegar la web, procesar archivos o resolver matemáticas. Todo el flujo es monitoreable en tiempo real con **Langfuse**.

> `# Proyecto de aprendizaje · AI Agents · RAG · Observabilidad de LLMs`

---

## `$ ls -la agents/`

```
drwxr-xr-x  agent/
│
├── supervisor.py      # Orquestador principal — decide qué agente activa
│
├── rag_agent.py       # Búsqueda semántica en documentos propios
├── web_agent.py       # Búsqueda y extracción de información en la web
├── file_agent.py      # Lectura e interpretación de archivos del sistema
└── math_agent.py      # Razonamiento y operaciones matemáticas
```

```
[supervisor] Consulta recibida: "¿Cuánto es la raíz cuadrada de 144?"
[supervisor] → Delegando a: math_agent
[math_agent] Resolviendo...
[math_agent] ✔ Resultado: 12
```

---

## `$ cat architecture.txt`

```
┌─────────────────────────────────────────────────────────────┐
│                        Usuario (CLI)                        │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
               ┌─────────────────────────┐
               │     Agente Supervisor    │
               │   (orquesta y enruta)    │
               └────────────┬────────────┘
                            │
          ┌─────────┬───────┴───────┬─────────┐
          ▼         ▼               ▼         ▼
     ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
     │   RAG   │ │   Web   │ │  File   │ │  Math   │
     │  Agent  │ │  Agent  │ │  Agent  │ │  Agent  │
     └────┬────┘ └─────────┘ └─────────┘ └─────────┘
          │
          ▼
   ┌─────────────────────────┐
   │       RAG Pipeline       │
   │  ├── Document Loader     │
   │  ├── Text Splitter       │
   │  ├── Embeddings          │
   │  └── PostgreSQL+pgvector │
   └─────────────────────────┘

  ════════════════════════════════════════
   Observabilidad end-to-end con Langfuse
   Trazas · Tokens · Latencia · Costos
  ════════════════════════════════════════
```

---

## `$ tail -f langfuse.log`

IA-Agent integra **Langfuse** para monitorear cada paso del sistema en tiempo real: qué agente se activó, cuántos tokens consumió, cuánto tardó y qué respondió.

```
[langfuse] trace_id=a3f9c2 · agent=rag_agent  · tokens=843 · latency=1.2s ✔
[langfuse] trace_id=b1d7e8 · agent=web_agent  · tokens=612 · latency=2.4s ✔
[langfuse] trace_id=c5a2f1 · agent=math_agent · tokens=120 · latency=0.3s ✔
```

<img width="1914" height="868" alt="Captura de pantalla 2026-03-19 202105" src="https://github.com/user-attachments/assets/31331b64-306e-44e3-b9ca-4570cadba5a8" />


---

## `$ pip install -r requirements.txt`

**Stack tecnológico:**

```python
dependencies = {
    "language"  : "Python 3.10+",
    "framework" : "LangChain",
    "database"  : "PostgreSQL + pgvector",
    "llm"       : "Google Gemini / OpenAI API",
    "observ"    : "Langfuse",
    "cli"       : "Rich",
}
```

---

## `$ ./setup.sh`

**1. Clonar el repositorio**

```bash
git clone https://github.com/JoakoMancilla/IA-Agent.git
cd IA-Agent
```

**2. Crear entorno virtual**

```bash
# Linux / Mac
python -m venv venv && source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Instalar dependencias**

```bash
pip install -r requirements.txt
```

**4. Configurar `.env`**

```env
# LLM
GOOGLE_API_KEY=tu_api_key

# Base de datos vectorial
DATABASE_URL=postgresql://usuario:password@localhost:5432/tu_base

# Langfuse — observabilidad
LANGFUSE_PUBLIC_KEY=tu_public_key
LANGFUSE_SECRET_KEY=tu_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

**5. Inicializar pgvector**

```sql
CREATE EXTENSION vector;
```

**6. Ingestar documentos**

```bash
python ingest.py

# [✔] Documentos cargados
# [✔] Chunks generados
# [✔] Embeddings almacenados en PostgreSQL
```

**7. Ejecutar**

```bash
python main.py
```

---

## `$ cat project_tree.txt`

```
IA-Agent/
│
├── main.py                  # Punto de entrada — CLI
│
├── agent/
│   ├── supervisor.py        # Agente supervisor (orquestador)
│   ├── rag_agent.py         # Sub-agente RAG
│   ├── web_agent.py         # Sub-agente de búsqueda web
│   ├── file_agent.py        # Sub-agente de archivos
│   └── math_agent.py        # Sub-agente matemático
│
├── RAG/
│   ├── ingest.py            # Carga e indexación de documentos
│   └── retriever.py         # Recuperación semántica
│
├── tools/                   # Herramientas disponibles para los agentes
│
├── .env.example
├── requirements.txt
└── README.md
```

---

## `$ cat roadmap.md`

```
[x] Agente conversacional con RAG
[x] Arquitectura multi-agente  (supervisor + 4 sub-agentes)
[x] Base de datos vectorial    (PostgreSQL + pgvector)
[x] CLI estilizado             (Rich)
[x] Observabilidad             (Langfuse — en desarrollo)
[ ] Streaming de respuestas
[ ] Memoria conversacional persistente
[ ] Nuevos sub-agentes especializados
[ ] Tools especializadas por dominio
[ ] Interfaz web
```

---

## `$ cat LICENSE`

```
MIT License · JoakoMancilla · 2025
```

<br>

<div align="center">

```
╭──────────────────────────────────────────────────────────────╮
│   Built while learning · AI Agents · RAG · LLM Observability │
╰──────────────────────────────────────────────────────────────╯
```

</div>
