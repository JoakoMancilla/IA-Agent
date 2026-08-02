<div align="center">

# IA-Agent

**Sistema conversacional multi-agente con arquitectura RAG, orquestación por supervisor y observabilidad end-to-end**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=flat-square&logo=chainlink&logoColor=white)](https://langchain.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-336791?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Langfuse](https://img.shields.io/badge/Langfuse-Observability-FF6B35?style=flat-square&logo=grafana&logoColor=white)](https://langfuse.com)
[![Rich](https://img.shields.io/badge/Rich-CLI-7E57C2?style=flat-square&logo=gnometerminal&logoColor=white)](https://rich.readthedocs.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)

</div>

<br>

<img width="2066" height="994" alt="IA-Agent CLI en ejecución" src="https://github.com/user-attachments/assets/cb789c1a-3b91-4e12-b249-f4b2b5d8ce3d" />

<br>

## Descripción

**IA-Agent** es un sistema de inteligencia artificial conversacional que se ejecuta desde la terminal. Un **agente supervisor** recibe cada consulta del usuario y la delega al sub-agente más adecuado — búsqueda semántica en documentos propios, navegación web, procesamiento de archivos o razonamiento matemático. Todo el flujo de ejecución es monitoreable en tiempo real mediante **Langfuse**.

El proyecto fue desarrollado como ejercicio práctico de arquitecturas multi-agente, RAG y observabilidad de sistemas basados en LLMs.

## Características

- **Orquestación por supervisor**: un agente central decide qué sub-agente debe atender cada consulta.
- **RAG (Retrieval-Augmented Generation)**: búsqueda semántica sobre documentos propios usando embeddings y una base de datos vectorial.
- **Agente web**: búsqueda y extracción de información desde internet.
- **Agente de archivos**: lectura e interpretación de archivos del sistema.
- **Agente matemático**: resolución de operaciones y razonamiento numérico.
- **Memoria conversacional persistente** entre sesiones.
- **Observabilidad end-to-end** con Langfuse: trazas, tokens, latencia y costos por cada ejecución.
- **CLI estilizado** con Rich.

## Arquitectura

```
                          Usuario (CLI)
                                │
                                ▼
                      ┌────────────────────┐
                      │  Agente Supervisor │
                      │ (orquesta y enruta)│
                      └─────────┬──────────┘
                                │
            ┌───────────┬───────┴───────┬───────────┐
            ▼           ▼               ▼           ▼
       ┌─────────┐ ┌─────────┐    ┌─────────┐ ┌─────────┐
       │   RAG   │ │   Web   │    │  File   │ │  Math   │
       │  Agent  │ │  Agent  │    │  Agent  │ │  Agent  │
       └────┬────┘ └─────────┘    └─────────┘ └─────────┘
            │
            ▼
   ┌─────────────────────────┐
   │     RAG Pipeline        │
   │  Document Loader        │
   │  Text Splitter          │
   │  Embeddings             │
   │  PostgreSQL + pgvector  │
   └─────────────────────────┘
```

Cada ejecución queda registrada en Langfuse, lo que permite auditar qué agente se activó, cuántos tokens consumió, cuánto tardó y qué respondió.

```
trace_id=a3f9c2  agent=rag_agent   tokens=843  latency=1.2s
trace_id=b1d7e8  agent=web_agent   tokens=612  latency=2.4s
trace_id=c5a2f1  agent=math_agent  tokens=120  latency=0.3s
```

<img width="1914" height="868" alt="Panel de observabilidad en Langfuse" src="https://github.com/user-attachments/assets/31331b64-306e-44e3-b9ca-4570cadba5a8" />

## Stack tecnológico

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.12+ |
| Framework de agentes | LangChain |
| Base de datos vectorial | PostgreSQL + pgvector |
| LLM | Google Gemini / OpenAI API |
| Observabilidad | Langfuse |
| Interfaz de línea de comandos | Rich |

## Estructura del proyecto

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
│   ├── index_docs.py        # Carga e indexación de documentos
│   └── manage_rag.py        # Búsqueda, conexión e inyección de datos
│
├── tools/                   # Herramientas disponibles para los agentes
│
├── .env
├── requirements.txt
└── README.md
```

## Instalación

**1. Clonar el repositorio**

```bash
git clone https://github.com/JoakoMancilla/IA-Agent.git
cd IA-Agent
```

**2. Instalar dependencias**

```bash
pip install -r requirements.txt
```

**3. Inicializar pgvector en PostgreSQL**

```sql
CREATE EXTENSION vector;
```

**4. Configurar variables de entorno**

Crear un archivo `.env` en la raíz del proyecto con las credenciales necesarias (API key del LLM, cadena de conexión a PostgreSQL, credenciales de Langfuse, etc.). *Ajusta los nombres exactos de las variables a los que use tu configuración actual.*

**5. Ingestar documentos**

```bash
python index_docs.py
```

**6. Ejecutar**

```bash
python main.py
```

## Roadmap

- [x] Agente conversacional con RAG
- [x] Memoria conversacional persistente
- [x] Arquitectura multi-agente (supervisor + 4 sub-agentes)
- [x] Base de datos vectorial (PostgreSQL + pgvector)
- [x] CLI estilizado (Rich)
- [x] Observabilidad (Langfuse — en desarrollo)
- [ ] Nuevos sub-agentes especializados

## Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

<div align="center">

Desarrollado por [JoakoMancilla](https://github.com/JoakoMancilla) — proyecto de aprendizaje en agentes de IA, RAG y observabilidad de LLMs.

</div>
